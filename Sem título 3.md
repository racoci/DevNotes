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

But then I get the same results I was having before. 
Just the usageEvents back.

I also went back to the list implementation (commented on the file I sent) to test the approach of sending every message all at once at the time of invoking the API, but it also gave me the same issue as before.

## About the second issue
As I have sent before (in the other issue, also attached here as Request-responses.txt), my current sequence of events is correct and the message at 11-26 12:31:35.468 is the contentEnd of the system prompt. This would never be the issue at this point because we would have a validation error before that.

## About issues 3 and 4
Thanks for pointing that out, this could be an issue in the future, but at the point we are I'm not even receiving back the audioOutput. I'll fix the sampleRate of the playback once I have something back to test with.

## About issue 4
Thanks for pointing that out, this could be an issue in the future, but at the point we are I'm not even receiving back the audioOutput event as can be seen by the logs. I'll fix this parsing once I have something back being sent by the API.

Would it be possible to enter in a call with me via teams. Could you try to reach me at racoci@motorola.com or racoci@lenovo.com. Another option would be to create a call on meet.