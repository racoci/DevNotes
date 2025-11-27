## Input event flow

The structure of the input event flow is provided in this section.

1. `RequestStartEvent`
    
    `{     "event": {         "sessionStart": {             "inferenceConfiguration": {                 "maxTokens": "int",                 "topP": "float",                 "temperature": "float"             }         }     } }`
    
2. `PromptStartEvent`
    
    `{     "event": {         "promptStart": {             "promptName": "string", // unique identifier same across all events i.e. UUID             "textOutputConfiguration": {                 "mediaType": "text/plain"             },             "audioOutputConfiguration": {                 "mediaType": "audio/lpcm",                 "sampleRateHertz": 8000 | 16000 | 24000,                 "sampleSizeBits": 16,                 "channelCount": 1,                 "voiceId": "matthew" | "tiffany" | "amy" |                         "lupe" | "carlos" | "ambre" | "florian" |                         "greta" | "lennart" | "beatrice" | "lorenzo",                 "encoding": "base64",                 "audioType": "SPEECH",             },             "toolUseOutputConfiguration": {                 "mediaType": "application/json"             },             "toolConfiguration": {                 "tools": [{                     "toolSpec": {                         "name": "string",                         "description": "string",                         "inputSchema": {                             "json": "{}"                         }                     }                 }]             }         }     } }`
    
3. `InputContentStartEvent`
    
    - `Text`
        
        `{     "event": {         "contentStart": {             "promptName": "string", // same unique identifier from promptStart event             "contentName": "string", // unique identifier for the content block             "type": "TEXT",             "interactive": false,             "role": "SYSTEM" | "USER" | "ASSISTANT",             "textInputConfiguration": {                 "mediaType": "text/plain"             }         }     } }`
        
    - `Audio`
        
        `{     "event": {         "contentStart": {             "promptName": "string", // same unique identifier from promptStart event             "contentName": "string", // unique identifier for the content block             "type": "AUDIO",             "interactive": true,             "role": "USER",             "audioInputConfiguration": {                 "mediaType": "audio/lpcm",                 "sampleRateHertz": 8000 | 16000 | 24000,                 "sampleSizeBits": 16,                 "channelCount": 1,                 "audioType": "SPEECH",                 "encoding": "base64"             }         }     } }`
        
    - `Tool`
        
        `{     "event": {         "contentStart": {             "promptName": "string", // same unique identifier from promptStart event             "contentName": "string", // unique identifier for the content block             "interactive": false,             "type": "TOOL",             "role": "TOOL",             "toolResultInputConfiguration": {                 "toolUseId": "string", // existing tool use id                 "type": "TEXT",                 "textInputConfiguration": {                     "mediaType": "text/plain"                 }             }         }     } }`
        
    
4. `TextInputContent`
    
    `{     "event": {         "textInput": {             "promptName": "string", // same unique identifier from promptStart event             "contentName": "string", // unique identifier for the content block             "content": "string"         }     } }`
    
5. `AudioInputContent`
    
    `{     "event": {         "audioInput": {             "promptName": "string", // same unique identifier from promptStart event             "contentName": "string", // same unique identifier from its contentStart             "content": "base64EncodedAudioData"         }     } }`
    
6. `ToolResultContentEvent`
    
    `"event": {     "toolResult": {         "promptName": "string", // same unique identifier from promptStart event         "contentName": "string", // same unique identifier from its contentStart         "content": "{\"key\": \"value\"}" // stringified JSON object as a tool result      } }`
    
7. `InputContentEndEvent`
    
    `{     "event": {         "contentEnd": {             "promptName": "string", // same unique identifier from promptStart event             "contentName": "string" // same unique identifier from its contentStart         }     } }`
    
8. `PromptEndEvent`
    
    `{     "event": {         "promptEnd": {             "promptName": "string" // same unique identifier from promptStart event         }     } }`
    
9. `RequestEndEvent`
    
    `{     "event": {         "sessionEnd": {}     } }`
    

- ### On this page
    
    1. [Input event flow](https://docs.aws.amazon.com/nova/latest/userguide/input-events.html#input-event-flow)
    
- #### Did this page help you?
    
    Yes
    
    No
    
    [Provide feedback](https://docs.aws.amazon.com/forms/aws-doc-feedback?hidden_service_name=Bedrock&topic_url=https://docs.aws.amazon.com/en_us/nova/latest/userguide/input-events.html)
    

#### Next topic:

[Output events](https://docs.aws.amazon.com/nova/latest/userguide/output-events.html)

#### Previous topic:

[Code examples](https://docs.aws.amazon.com/nova/latest/userguide/speech-code-examples.html)