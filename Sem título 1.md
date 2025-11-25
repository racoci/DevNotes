This example provides a step-by-step explanation of how to implement a simple, real-time audio streaming application using the Amazon Nova Sonic model. This simplified version demonstrates the core functionality needed to create a audio conversation with the Amazon Nova Sonic model.

You can access the following example in our [Amazon Nova samples GitHub repo](https://github.com/aws-samples/amazon-nova-samples/blob/main/speech-to-speech/sample-codes/console-python/nova_sonic_simple.py).

 ###### State the imports and configuration
    
    This section imports necessary libraries and sets audio configuration parameters:
    
    - `asyncio`: For asynchronous programming
        
    - `base64`: For encoding and decoding audio data
        
    - `pyaudio`: For audio capture and playback
        
    - Amazon Bedrock SDK components for streaming
        
    - Audio constants define the format of audio capture (16kHz sample rate, mono channel)
        
    
    `import os import asyncio import base64 import json import uuid import pyaudio from aws_sdk_bedrock_runtime.client import BedrockRuntimeClient, InvokeModelWithBidirectionalStreamOperationInput from aws_sdk_bedrock_runtime.models import InvokeModelWithBidirectionalStreamInputChunk, BidirectionalInputPayloadPart from aws_sdk_bedrock_runtime.config import Config, HTTPAuthSchemeResolver, SigV4AuthScheme from smithy_aws_core.credentials_resolvers.environment import EnvironmentCredentialsResolver  # Audio configuration INPUT_SAMPLE_RATE = 16000 OUTPUT_SAMPLE_RATE = 24000 CHANNELS = 1 FORMAT = pyaudio.paInt16 CHUNK_SIZE = 1024`
    
2. ###### Define the `SimpleNovaSonic` class
    
    The `SimpleNovaSonic` class is the main class that handles the Amazon Nova Sonic interaction:
    
    - `model_id`: The Amazon Nova Sonic model ID (`amazon.nova-sonic-v1:0`)
        
    - `region`: The AWS Region, the default is `us-east-1`
        
    - Unique IDs for prompt and content tracking
        
    - An asynchronous queue for audio playback
        
    
    `class SimpleNovaSonic:     def __init__(self, model_id='amazon.nova-sonic-v1:0', region='us-east-1'):         self.model_id = model_id         self.region = region         self.client = None         self.stream = None         self.response = None         self.is_active = False         self.prompt_name = str(uuid.uuid4())         self.content_name = str(uuid.uuid4())         self.audio_content_name = str(uuid.uuid4())         self.audio_queue = asyncio.Queue()         self.display_assistant_text = False`
    
3. ###### Initialize the client
    
    This method configures the Amazon Bedrock client with the following:
    
    - The appropriate endpoint for the specified region
        
    - Authentication information using environment variables for AWS credentials
        
    - The SigV4 authentication scheme for the AWS API calls
        
    
        `def _initialize_client(self):         """Initialize the Bedrock client."""         config = Config(             endpoint_uri=f"https://bedrock-runtime.{self.region}.amazonaws.com",             region=self.region,             aws_credentials_identity_resolver=EnvironmentCredentialsResolver(),             http_auth_scheme_resolver=HTTPAuthSchemeResolver(),             http_auth_schemes={"aws.auth#sigv4": SigV4AuthScheme()}         )         self.client = BedrockRuntimeClient(config=config)`
    
4. ###### Handle events
    
    This helper method sends JSON events to the bidirectional stream, which is used for all communication with the Amazon Nova Sonic model:
    
        `async def send_event(self, event_json):         """Send an event to the stream."""         event = InvokeModelWithBidirectionalStreamInputChunk(             value=BidirectionalInputPayloadPart(bytes_=event_json.encode('utf-8'))         )         await self.stream.input_stream.send(event)`
    
5. ###### Start the session
    
    This method initiates the session and setups the remaining events to start audio streaming. These events need to be sent in the same order.
    
        `async def start_session(self):         """Start a new session with Nova Sonic."""         if not self.client:             self._initialize_client()                      # Initialize the stream         self.stream = await self.client.invoke_model_with_bidirectional_stream(             InvokeModelWithBidirectionalStreamOperationInput(model_id=self.model_id)         )         self.is_active = True                  # Send session start event         session_start = '''         {           "event": {             "sessionStart": {               "inferenceConfiguration": {                 "maxTokens": 1024,                 "topP": 0.9,                 "temperature": 0.7               }             }           }         }         '''         await self.send_event(session_start)                  # Send prompt start event         prompt_start = f'''         {{           "event": {{             "promptStart": {{               "promptName": "{self.prompt_name}",               "textOutputConfiguration": {{                 "mediaType": "text/plain"               }},               "audioOutputConfiguration": {{                 "mediaType": "audio/lpcm",                 "sampleRateHertz": 24000,                 "sampleSizeBits": 16,                 "channelCount": 1,                 "voiceId": "matthew",                 "encoding": "base64",                 "audioType": "SPEECH"               }}             }}           }}         }}         '''         await self.send_event(prompt_start)                  # Send system prompt         text_content_start = f'''         {{             "event": {{                 "contentStart": {{                     "promptName": "{self.prompt_name}",                     "contentName": "{self.content_name}",                     "type": "TEXT",                     "interactive": true,                     "role": "SYSTEM",                     "textInputConfiguration": {{                         "mediaType": "text/plain"                     }}                 }}             }}         }}         '''         await self.send_event(text_content_start)                  system_prompt = "You are a friendly assistant. The user and you will engage in a spoken dialog " \             "exchanging the transcripts of a natural real-time conversation. Keep your responses short, " \             "generally two or three sentences for chatty scenarios."                    text_input = f'''         {{             "event": {{                 "textInput": {{                     "promptName": "{self.prompt_name}",                     "contentName": "{self.content_name}",                     "content": "{system_prompt}"                 }}             }}         }}         '''         await self.send_event(text_input)                  text_content_end = f'''         {{             "event": {{                 "contentEnd": {{                     "promptName": "{self.prompt_name}",                     "contentName": "{self.content_name}"                 }}             }}         }}         '''         await self.send_event(text_content_end)                  # Start processing responses         self.response = asyncio.create_task(self._process_responses())`
    
6. ###### Handle audio input
    
    These methods handle the audio input lifecycle:
    
    - `start_audio_input`: Configures and starts the audio input stream
        
    - `send_audio_chunk`: Encodes and sends audio chunks to the model
        
    - `end_audio_input`: Properly closes the audio input stream
        
    
       `async def start_audio_input(self):         """Start audio input stream."""         audio_content_start = f'''         {{             "event": {{                 "contentStart": {{                     "promptName": "{self.prompt_name}",                     "contentName": "{self.audio_content_name}",                     "type": "AUDIO",                     "interactive": true,                     "role": "USER",                     "audioInputConfiguration": {{                         "mediaType": "audio/lpcm",                         "sampleRateHertz": 16000,                         "sampleSizeBits": 16,                         "channelCount": 1,                         "audioType": "SPEECH",                         "encoding": "base64"                     }}                 }}             }}         }}         '''         await self.send_event(audio_content_start)          async def send_audio_chunk(self, audio_bytes):         """Send an audio chunk to the stream."""         if not self.is_active:             return                      blob = base64.b64encode(audio_bytes)         audio_event = f'''         {{             "event": {{                 "audioInput": {{                     "promptName": "{self.prompt_name}",                     "contentName": "{self.audio_content_name}",                     "content": "{blob.decode('utf-8')}"                 }}             }}         }}         '''         await self.send_event(audio_event)          async def end_audio_input(self):         """End audio input stream."""         audio_content_end = f'''         {{             "event": {{                 "contentEnd": {{                     "promptName": "{self.prompt_name}",                     "contentName": "{self.audio_content_name}"                 }}             }}         }}         '''         await self.send_event(audio_content_end)`
    
7. ###### End the session
    
    This method properly closes the session by:
    
    - Sending a `promptEnd` event
        
    - Sending a `sessionEnd` event
        
    - Closing the input stream
        
    
        `async def end_session(self):         """End the session."""         if not self.is_active:             return                      prompt_end = f'''         {{             "event": {{                 "promptEnd": {{                     "promptName": "{self.prompt_name}"                 }}             }}         }}         '''         await self.send_event(prompt_end)                  session_end = '''         {             "event": {                 "sessionEnd": {}             }         }         '''         await self.send_event(session_end)         # close the stream         await self.stream.input_stream.close()`
    
8. ###### Handle responses
    
    This method continuously processes responses from the model and does the following:
    
    - Waits for output from the stream.
        
    - Parses the JSON response.
        
    - Handles text output by printing to the console with automatic speech recognition and transcription.
        
    - Handles audio output by decoding and queuing for playback.
        
    
        `async def _process_responses(self):         """Process responses from the stream."""         try:             while self.is_active:                 output = await self.stream.await_output()                 result = await output[1].receive()                                  if result.value and result.value.bytes_:                     response_data = result.value.bytes_.decode('utf-8')                     json_data = json.loads(response_data)                                          if 'event' in json_data:                         # Handle content start event                         if 'contentStart' in json_data['event']:                             content_start = json_data['event']['contentStart']                              # set role                             self.role = content_start['role']                             # Check for speculative content                             if 'additionalModelFields' in content_start:                                 additional_fields = json.loads(content_start['additionalModelFields'])                                 if additional_fields.get('generationStage') == 'SPECULATIVE':                                     self.display_assistant_text = True                                 else:                                     self.display_assistant_text = False                                                          # Handle text output event                         elif 'textOutput' in json_data['event']:                             text = json_data['event']['textOutput']['content']                                                             if (self.role == "ASSISTANT" and self.display_assistant_text):                                 print(f"Assistant: {text}")                             elif self.role == "USER":                                 print(f"User: {text}")                                                  # Handle audio output                         elif 'audioOutput' in json_data['event']:                             audio_content = json_data['event']['audioOutput']['content']                             audio_bytes = base64.b64decode(audio_content)                             await self.audio_queue.put(audio_bytes)         except Exception as e:             print(f"Error processing responses: {e}")`
    
9. ###### Playback audio
    
    This method will perform the following tasks:
    
    - Initialize a `PyAudio` input stream
        
    - Continuously retrieves audio data from the queue
        
    - Plays the audio through the speakers
        
    - Properly cleans up resources when done
        
    
       `async def play_audio(self):         """Play audio responses."""         p = pyaudio.PyAudio()         stream = p.open(             format=FORMAT,             channels=CHANNELS,             rate=OUTPUT_SAMPLE_RATE,             output=True         )                  try:             while self.is_active:                 audio_data = await self.audio_queue.get()                 stream.write(audio_data)         except Exception as e:             print(f"Error playing audio: {e}")         finally:             stream.stop_stream()             stream.close()             p.terminate()`
    
10. ###### Capture audio
    
    This method will perform the following tasks:
    
    - Initialize a `PyAudio` output stream
        
    - Starts the audio input session
        
    - Continuously captures audio chunks from the microphone
        
    - Sends each chunk to the Amazon Nova Sonic model
        
    - Properly cleans up resources when done
        
    
        `async def capture_audio(self):         """Capture audio from microphone and send to Nova Sonic."""         p = pyaudio.PyAudio()         stream = p.open(             format=FORMAT,             channels=CHANNELS,             rate=INPUT_SAMPLE_RATE,             input=True,             frames_per_buffer=CHUNK_SIZE         )                  print("Starting audio capture. Speak into your microphone...")         print("Press Enter to stop...")                  await self.start_audio_input()                  try:             while self.is_active:                 audio_data = stream.read(CHUNK_SIZE, exception_on_overflow=False)                 await self.send_audio_chunk(audio_data)                 await asyncio.sleep(0.01)         except Exception as e:             print(f"Error capturing audio: {e}")         finally:             stream.stop_stream()             stream.close()             p.terminate()             print("Audio capture stopped.")             await self.end_audio_input()`
    
11. ###### Run the main function
    
    The main function orchestrates the entire process by performing the following:
    
    - Creates a Amazon Nova Sonic client
        
    - Starts the session
        
    - Creates concurrent tasks for audio playback and capture
        
    - Waits for the user to press **Enter** to stop
        
    - Properly ends the session and cleans up tasks
        
    
    `async def main():     # Create Nova Sonic client     nova_client = SimpleNovaSonic()          # Start session     await nova_client.start_session()          # Start audio playback task     playback_task = asyncio.create_task(nova_client.play_audio())          # Start audio capture task     capture_task = asyncio.create_task(nova_client.capture_audio())          # Wait for user to press Enter to stop     await asyncio.get_event_loop().run_in_executor(None, input)          # End session     nova_client.is_active = False          # First cancel the tasks     tasks = []     if not playback_task.done():         tasks.append(playback_task)     if not capture_task.done():         tasks.append(capture_task)     for task in tasks:         task.cancel()     if tasks:         await asyncio.gather(*tasks, return_exceptions=True)          # cancel the response task     if nova_client.response and not nova_client.response.done():         nova_client.response.cancel()          await nova_client.end_session()     print("Session ended")  if __name__ == "__main__":     # Set AWS credentials if not using environment variables     # os.environ['AWS_ACCESS_KEY_ID'] = "your-access-key"     # os.environ['AWS_SECRET_ACCESS_KEY'] = "your-secret-key"     # os.environ['AWS_DEFAULT_REGION'] = "us-east-1"      asyncio.run(main())`
    

- #### Did this page help you?
    
    Yes
    
    No
    
    [Provide feedback](https://docs.aws.amazon.com/forms/aws-doc-feedback?hidden_service_name=Bedrock&topic_url=https://docs.aws.amazon.com/en_us/nova/latest/userguide/s2s-example.html)