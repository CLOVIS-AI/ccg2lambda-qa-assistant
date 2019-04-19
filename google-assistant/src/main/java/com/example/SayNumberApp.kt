/*
 * Copyright 2018 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.example

import com.google.actions.api.ActionRequest
import com.google.actions.api.ActionResponse
import com.google.actions.api.ActionsSdkApp
import com.google.actions.api.ForIntent
import com.google.actions.api.response.ResponseBuilder
import org.slf4j.LoggerFactory
import utils.bundle
import utils.get
import java.text.MessageFormat

class SayNumberApp : ActionsSdkApp() {

    // Note: Do not store any state as an instance variable.
    // It is ok to have final variables where the variable is assigned a value in
    // the constructor but remains unchanged. This is required to ensure thread-
    // safety as the entry point (ActionServlet) instances may
    // be reused by the server.

    @ForIntent("actions.intent.MAIN")
    fun welcome(request: ActionRequest): ActionResponse {
        LOGGER.info("Welcome intent start.")
        val responseBuilder = request.buildResponse
        val resources = bundle("resources", request.locale)
        responseBuilder.add(resources["welcome"])

        LOGGER.info("Welcome intent end.")
        return responseBuilder.build()
    }

    @ForIntent("actions.intent.TEXT")
    fun number(request: ActionRequest): ActionResponse {
        LOGGER.info("Number intent start.")
        val responseBuilder = request.buildResponse
        val resources = bundle("resources")

        val userNumber = request.getArgument("text")?.textValue
        val response: String
        when (userNumber) {
            "bye" -> {
                response = resources["bye"]
                responseBuilder.add(response).endConversation()
            }
            else -> {
                response = MessageFormat.format(resources["sayOrdinal"], userNumber)
                responseBuilder.add(response)
            }
        }
        LOGGER.info("Number intent end.")
        return responseBuilder.build()
    }

    companion object {

        private val LOGGER = LoggerFactory
                .getLogger(SayNumberApp::class.java)

    }

    /**
     * Convenience variable to get a [ResponseBuilder] from an [ActionRequest].
     */
    private val ActionRequest.buildResponse: ResponseBuilder
        get() = getResponseBuilder(this)
}
