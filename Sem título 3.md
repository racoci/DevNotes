You probably won't be able to reproduce the same errors in the python version because the issue might be in the kotlin implementation of the SDK.
About the issues you have mentioned. I did some tests and it doesn't seeen any of them is the real root cause of this issue.

## About the first issue
I tested two sequential approaches: Building the request first using the class channel as stream:
```kotlin
suspend fun translateOnce(pcm16kMonoBytes: ByteArray): ByteArray = withContext(Dispatchers.IO) {  
    Log.d(TAG, "Before invokeModelWithBidirectionalStream")  
  
    bedrock?.invokeModelWithBidirectionalStream(  
        InvokeModelWithBidirectionalStreamRequest {  
            this.modelId = "amazon.nova-sonic-v1:0"  
            this.body = inputParts.consumeAsFlow()  
        }  
    ) { response ->  
        response.body.also { responseBody ->  
            Log.d(TAG, "Response received: $response with body $responseBody")  
        }?.onEach { out: InvokeModelWithBidirectionalStreamOutput ->  
            handleAudioOutput(out)  
        }?.apply {  
            collect()  
        }  
    }  
    Log.d(TAG, "After invokeModelWithBidirectionalStream")  
  
    startSession()  
    sendSystemPrompt()  
    sendAudioChunk(pcm16kMonoBytes)  
    endSession()  // <-- ADDED: Properly close the session  
  
    audioOut.toByteArray()  
}
```
This did not work because the suspend call to  invokeModelWithBidirectionalStream blocks the corroutine so the other calls to startSession, sendSystemPrompt, etc.  never happen. 
It prints only `NovaSonic: Before invokeModelWithBidirectionalStream` on the logs

I also tested putting it at the end:
```kotlin
suspend fun translateOnce(pcm16kMonoBytes: ByteArray): ByteArray = withContext(Dispatchers.IO) {
    startSession()
    sendSystemPrompt()
    sendAudioChunk(pcm16kMonoBytes)
    endSession()  // <-- ADDED: Properly close the session

    Log.d(TAG, "Before invokeModelWithBidirectionalStream")

    bedrock?.invokeModelWithBidirectionalStream(
        InvokeModelWithBidirectionalStreamRequest {
            this.modelId = "amazon.nova-sonic-v1:0"
            this.body = inputParts.consumeAsFlow()
        }
    ) { response ->
        response.body.also { responseBody ->
            Log.d(TAG, "Response received: $response with body $responseBody")
        }?.onEach { out: InvokeModelWithBidirectionalStreamOutput ->
            handleAudioOutput(out)
        }?.apply {
            collect()
        }
    }

    Log.d(TAG, "After invokeModelWithBidirectionalStream")
    audioOut.toByteArray()
}
```

But then I get the same results I was having before. Just the usageEvents back, in this case  I went back to the list implementation where I add all the events in a list before building the request and only build the request after everything is sent.

## About the second issue
As I have sent before (in the other issue), my current sequence of events is:
```
11-26 12:31:35.463  7424  7645 D NovaSonic: Sending valid json event: {"event": {"sessionStart": {"inferenceConfiguration": {"maxTokens": 1024,"topP": 0.9,"temperature": 0.7}}}}
11-26 12:31:35.464  7424  7645 D NovaSonic: Sending valid json event: {"event": {"promptStart": {"promptName": "ba6f3b0d-df1c-4471-b864-96fa8f51f066","textOutputConfiguration": {"mediaType": "text/plain"},"audioOutputConfiguration": {"mediaType": "audio/lpcm","sampleRateHertz": 24000,"sampleSizeBits": 16,"channelCount": 1,"voiceId": "matthew","encoding": "base64","audioType": "SPEECH"}}}}
11-26 12:31:35.465  7424  7645 D NovaSonic: Sending valid json event: {"event": {"contentStart": {"promptName": "ba6f3b0d-df1c-4471-b864-96fa8f51f066","contentName": "b4bc4115-2add-40c3-8971-cd43a0e170f2","type": "TEXT","interactive": true,"role": "SYSTEM","textInputConfiguration": {"mediaType": "text/plain"}}}}
11-26 12:31:35.467  7424  7645 D NovaSonic: Sending valid json event: {"event": {"textInput": {"promptName": "ba6f3b0d-df1c-4471-b864-96fa8f51f066","contentName": "b4bc4115-2add-40c3-8971-cd43a0e170f2","content": "You are a professional translator and your function is to translate what the user says back in English. Just repeat back what the user says in English. Do not try to answer their questions or interact with them in any way."}}}
11-26 12:31:35.468  7424  7645 D NovaSonic: Sending valid json event: {"event": {"contentEnd": {"promptName": "ba6f3b0d-df1c-4471-b864-96fa8f51f066","contentName": "b4bc4115-2add-40c3-8971-cd43a0e170f2"}}}
11-26 12:31:35.469  7424  7645 D NovaSonic: Sending valid json event: {"event": {"contentStart": {"promptName": "ba6f3b0d-df1c-4471-b864-96fa8f51f066","contentName": "eaf397d9-bdbc-4bf6-b6a6-9ea9a00ef10a","type": "AUDIO","interactive": true,"role": "USER","audioInputConfiguration": {"mediaType": "audio/lpcm","sampleRateHertz": 16000,"sampleSizeBits": 16,"channelCount": 1,"audioType": "SPEECH","encoding": "base64"}}}}
11-26 12:31:35.571  7424  7645 D NovaSonic: Sending valid json event: {"event": {"audioInput": {"promptName": "ba6f3b0d-df1c-4471-b864-96fa8f51f066","contentName": "eaf397d9-bdbc-4bf6-b6a6-9ea9a00ef10a","content": "AAD/////AAD//wAAAAAAAAAAAAAAAAAAAAAAAP//AAD//////v///wAA//8AAP///v/+//7//v/+//7//v/+//3//f////z/+v/7//z//f/8//3/+//6//z//f/+//v//v/+//z/AAABAP7//f/+//3//P/6//r/+f/4//n/+f/5//r/+v////r/9v/4//z/+//9//f/+f/+//v/+P/7//7/+////////v/9//z/+//4//7//v////j/+v/8//X/+v8DAAQA/v/+//v/9//5//L/9//2//T////9//3//f/5//f/9f/5//n/7//v/+b/8P/z//H/8f/x//T/9/8AAPD/8f/1//X/9P/5//j/9/8BAPn/9/8CAPn/9//2//r/8//x//T//f/+//X/+P8AAAQA/f/9////BgAEAAoADQAOAA4AGQAVABUAEAATABUADAAOAAoA/v8EAAQAAwD8//j/8f/r//L/9f/1/+v/9v/9//n/8//2////8P/v/+j/+v/1/wMA9/8FAAMA9v/y//n//P/1//v/+P/2//r/AwAAAAAABgAIAAMAAQD1//D/5f/1/+3/+P8JAPz/AQACAAIA+v8HAP7/CwD1//X/AQD9/wAAAgD6//r/+f/0//v/6P/n/+P/4v/c/9r/5v/x/9T/7P/3//L/8f/9/wMA9/8IAAsABgANAAMABAAAAAEA6P/7//b/7f/g/93/1P/o/+r/7v/+/+j/6//s/w0ADgDq/83/WQAAAP3/3/+e/7P/6v/a/ywAa/+HABIA0f8FAGb/CwEnARMBwQDw/gcB7wA5ACL/Gv4U//b+fP8C/6P/uQACAYgBeQCR/54AXQDDAI8A7f9j/33/T/7w/sr/8f6U/9H/k/++/2MAOf9U/1T/Vv/J/8z/nP8oADv/xv/x/2cAlQBqAekA1ACwAOsArwBPAcAA+wBaAB0AfgDQ//f//v8BAAH/Nf/y/o3+Nv4N/3b/dv+F/nX/U/+1//H/JwCw/9X/RQDo/yf/Uf/J/8X/4f+7//z/FwBqAFsAmADQ/6IAFgHBAIUAXgC0/5b/WP/W/2T/fv+t/37/Iv9V/5v/cv+J/ysAlP/l/8b/aACrAFsAoAAPAdoAgwB5AIMAsf/r//3/Yv/l/6H/lP/Z/wAAPgAjABYARQDV/7z/q/+U//T/EQC8//b/uv8nAGYAPADu/wwA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
11-26 12:31:35.572  7424  7645 D NovaSonic: Sending valid json event: {"event": {"contentEnd": {"promptName": "ba6f3b0d-df1c-4471-b864-96fa8f51f066","contentName": "eaf397d9-bdbc-4bf6-b6a6-9ea9a00ef10a"}}}
11-26 12:31:36.381  7424  7645 D NovaSonic: Response: {"event":{"usageEvent":{"completionId":"94430d34-09bf-4228-9b74-5eaacf5cd427","details":{"delta":{"input":{"speechTokens":0,"textTokens":22},"output":{"speechTokens":0,"textTokens":0}},"total":{"input":{"speechTokens":0,"textTokens":22},"output":{"speechTokens":0,"textTokens":0}}},"promptName":"ba6f3b0d-df1c-4471-b864-96fa8f51f066","sessionId":"455287da-a62a-41bc-adec-3a2efc20878c","totalInputTokens":22,"totalOutputTokens":0,"totalTokens":22}}}
11-26 12:31:36.422  7424  7645 D NovaSonic: Response: {"event":{"usageEvent":{"completionId":"94430d34-09bf-4228-9b74-5eaacf5cd427","details":{"delta":{"input":{"speechTokens":150,"textTokens":0},"output":{"speechTokens":0,"textTokens":0}},"total":{"input":{"speechTokens":150,"textTokens":22},"output":{"speechTokens":0,"textTokens":0}}},"promptName":"ba6f3b0d-df1c-4471-b864-96fa8f51f066","sessionId":"455287da-a62a-41bc-adec-3a2efc20878c","totalInputTokens":172,"totalOutputTokens":0,"totalTokens":172}}}
11-26 12:31:36.426  7424  7645 D NovaSonic: Response: {"event":{"usageEvent":{"completionId":"94430d34-09bf-4228-9b74-5eaacf5cd427","details":{"delta":{"input":{"speechTokens":0,"textTokens":1},"output":{"speechTokens":0,"textTokens":0}},"total":{"input":{"speechTokens":150,"textTokens":23},"output":{"speechTokens":0,"textTokens":0}}},"promptName":"ba6f3b0d-df1c-4471-b864-96fa8f51f066","sessionId":"455287da-a62a-41bc-adec-3a2efc20878c","totalInputTokens":173,"totalOutputTokens":0,"totalTokens":173}}}
11-26 12:32:35.575  7424  7648 D NovaSonic: Sending valid json event: {"event": {"promptEnd": {"promptName": "ba6f3b0d-df1c-4471-b864-96fa8f51f066"}}}
11-26 12:32:35.576  7424  7648 D NovaSonic: Sending valid json event: {"event": {"sessionEnd": {}}}
```

The message at 11-26 12:31:35.468 is the contentEnd