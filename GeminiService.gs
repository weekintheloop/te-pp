/**
 * @fileoverview GeminiService.gs
 * @description A low-level wrapper for the Gemini 2.5 Flash API.
 * Handles API key management (from Script Properties), request construction, and response parsing.
 * Includes caching (CacheService) to reduce costs.
 */

const GEMINI_API_KEY = PropertiesService.getScriptProperties().getProperty("GEMINI_API_KEY");
const CACHE = CacheService.getScriptCache();

/**
 * Calls the Gemini API with a given prompt and options.
 * @param {string} prompt - The text prompt for the Gemini API.
 * @param {object} [options={}] - Optional parameters for the API call (e.g., temperature, maxOutputTokens).
 * @returns {string} - The text response from the Gemini API.
 */
function callGeminiApi(prompt, options = {}) {
    if (!GEMINI_API_KEY) {
        throw new Error("GEMINI_API_KEY is not set in Script Properties.");
    }

    const defaultOptions = {
        temperature: 0.1,
        maxOutputTokens: 2048,
        topK: 1,
        topP: 1,
    };
    const mergedOptions = { ...defaultOptions, ...options };

    const cacheKey = Utilities.base64Encode(Utilities.newBlob(JSON.stringify({ prompt, mergedOptions })).getBytes());
    let cachedResponse = CACHE.get(cacheKey);
    if (cachedResponse) {
        console.log("Gemini API response from cache.");
        return cachedResponse;
    }

    const data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": mergedOptions.temperature,
            "topK": mergedOptions.topK,
            "topP": mergedOptions.topP,
            "maxOutputTokens": mergedOptions.maxOutputTokens,
            "stopSequences": []
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]
    };

    const fetchOptions = {
        'method': 'post',
        'contentType': 'application/json',
        'payload': JSON.stringify(data),
        'muteHttpExceptions': true,
    };

    const url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + GEMINI_API_KEY;
    const response = UrlFetchApp.fetch(url, fetchOptions);

    const responseCode = response.getResponseCode();
    if (responseCode >= 400) {
        const errorDetails = JSON.parse(response.getContentText());
        throw new Error(`Gemini API Error (${responseCode}): ${errorDetails.error.message}`);
    }

    const payload = JSON.parse(response.getContentText());
    if (!payload.candidates || payload.candidates.length === 0) {
        throw new Error("No candidates found in Gemini API response.");
    }

    const text = payload.candidates[0].content.parts[0].text;
    CACHE.put(cacheKey, text, 3600); // Cache for 1 hour
    return text;
}


