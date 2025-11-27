Hello Team,

Thank you for your patience while I investigated this issue. I performed a detailed replication of your Nova Sonic implementation in my environment to understand the behavior of the bidirectional streaming API

===== Summary of Investigation =====
Initial Replication Attempts

I created a Python test script following the same event sequence as your Kotlin implementation:

1. First attempt with synthetic audio (Mac TTS): The model processed the input audio (speechTokens: 150) but generated no output (speechTokens: 0, textTokens: 0), returning only usageEvent - identical to your reported behavior.

2. Second attempt with real human voice: The model successfully:

* Transcribed the input: "hello this is a test can you hear me"
* Generated a text response: "Hello! Yes, I can hear you perfectly. How are you doing today?"
* Produced audio output chunks (speechTokens: 82)

===== Root Cause =====
Nova Sonic is optimized for real human voice input. Synthetic/TTS audio is not processed correctly by the model, resulting in the behavior you observed (input processed but no output generated)

===== Required Changes to Your Implementation =====
Based on my code review, I identified several issues that need to be addressed:

1. Race Condition in Audio Streaming (critical)

Current code

```
launch {
    startSession()
    sendAudioChunk(pcm16kMonoBytes)
    endSession()
}
// Request executes immediately without waiting
val request = InvokeModelWithBidirectionalStreamRequest { ... }
```

* The issue is that the launch{} coroutine runs in parallel with the request, causing timing issues.
* Make the operations sequential or use proper synchronization:

```
// option 1: sequential with suspending functions
suspend fun translateOnce(pcm16kMonoBytes: ByteArray) {
    startSession()
    sendAudioChunk(pcm16kMonoBytes)
    // Wait for response before ending
    delay(appropriateTimeout)
    endSession()
}
````

2. Missing contentEnd After System Prompt (critical)

- - -  Current sequence - - - 

sessionStart -> promptStart -> contentStart(SYSTEM) -> textInput -> contentStart(AUDIO)

- - -  Required sequence - - - 

sessionStart -> promptStart -> contentStart(SYSTEM) -> textInput -> contentEnd -> contentStart(AUDIO)

You must send contentEnd after the system prompt's textInput before starting the audio content

3. Audio Playback Sample Rate (important)

Issue: Using inputSampleRate (16000 Hz) for playback instead of outputSampleRate (24000 Hz)

Fix

```
// Nova Sonic outputs at 24000 Hz, not 16000 Hz
playPcm(echoedAudio, outputSampleRate) // Use 24000, not 16000
```

4. Incorrect Event Pattern Search

Current: Searching for "response.outputAudio"

Correct: Search for "audioOutput" as per the API response format

5. Channel Management

Issue: Calling inputParts.close() in endSession() permanently closes the channel

Fix: Either recreate the channel for each session or use a different completion signal

6. JSON Formatting

Ensure all JSON events are single-line strings with no embedded newlines:

```
// bad
val systemPrompt = """
    You are a helpful assistant.
    Respond naturally.
"""

// good  
val systemPrompt = "You are a helpful assistant. Respond naturally."
```

======= Audio Requirements =======
For Nova Sonic to work correctly, the audio input must be:

========================================
Parameter    Required Value
========================================
Sample            Rate
16000               Hz
Channels         1 (Mono)
Bit Depth        16-bit signed PCM
Source              Real human voice (microphone input)
========================================

Important: Synthetic/TTS audio does not produce reliable results

======= Successful Test Output (Reference) =======
Here is the output from my successful test with real human voice:
```
>>> Streaming 156 audio chunks...
<<< [completionStart]: Model is responding!
<<< [textOutput]: "hello this is a test can you hear me"  ← Transcription
<<< [textOutput]: "Hello! Yes, I can hear you perfectly. How are you doing today?" ← Response
<<< [audioOutput]: *** GOT AUDIO OUTPUT! ***
<<< [audioOutput]: *** GOT AUDIO OUTPUT! ***
<<< [audioOutput]: *** GOT AUDIO OUTPUT! ***
<<< [audioOutput]: *** GOT AUDIO OUTPUT! ***
<<< [usageEvent] OUTPUT: speech=82, text=69  ← Audio generated successfully
```

======= Next Steps =======

1. Apply the code fixes listed above
2. Test with real microphone input (not pre-recorded or synthetic audio)
3. Verify the event sequence follows the correct order

==== ATTACHMENTS ====

* test_nova_sonic.py - Python reference implementation using aws-sdk-python-bedrock-runtime that produced successful results

* Python SDK Setup (for reference):

```
pip install aws-sdk-python-bedrock-runtime boto3
export AWS_ACCESS_KEY_ID=<your-key>
export AWS_SECRET_ACCESS_KEY=<your-secret>
```


===== RESOURCES =====
[1] https://docs.aws.amazon.com/nova/latest/userguide/input-events.html 
[2] https://docs.aws.amazon.com/nova/latest/userguide/output-events.html 
[3] https://docs.aws.amazon.com/nova/latest/userguide/s2s-example.html 
[4] https://github.com/aws-samples/amazon-nova-samples 

We value your feedback. Please share your experience by rating this and other correspondences in the AWS Support Center. You can rate a correspondence by selecting the stars in the top right corner of the correspondence.

Best regards,
Emiliano L.
Amazon Web Services

Attachments
Test-novasonic-reference.py.zip