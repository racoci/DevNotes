You probably won't be able to reproduce the same errors in the python version because the issue might be in the kotlin implementation of the SDK.
About the issues you have mentioned. I did some tests and it doesn't seeen any of them is the real root cause of this issue.

## About the first issue
I tested two sequential approaches: Building the request first using the class channel as stream:
```kotlin
suspend fun translateOnce(pcm16kMonoBytes: ByteArray): ByteArray = withContext(Dispatchers.IO) {
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

    Log.d(TAG, "Before invokeModelWithBidirectionalStream")
    
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
