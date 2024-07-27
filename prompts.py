# Description: This file contains the prompts that are used to guide the user in their responses.
# Consider setting max_token in llms.py

custom_prompts = { 
    # for the user prompts
    "short and concise" : "Your response should be short but concise, no more than 3 sentences.",
    "correct english" : "Your response should be the correction of the given prompt. If the prompt is already correct, respond with 'Your english is correct'.",
    "correct german" : "Ihre Antwort sollte die Korrektur des gegebenen Anliegens sein. Wenn das Anliegend bereits korrekt ist, antworten Sie mit 'Ihr Deutsch ist korrekt'.",
    "translate to english" : "You are a native English speaker, and your task is to translate every prompt you receive into English!",
    "translate to german" : "Du bist ein Muttersprachler der deutschen Sprache, und deine Aufgabe ist es, jedes Anliegen, das du erhältst, ins Deutsche zu übersetzen!",
    "translate to hungarian" : "Anyanyelvi szintű magyarul beszélő vagy és az a feladatod, hogy a szövegeket, amiket a felhasználó ad, magyarra fordíts!",
    # under construction
    "translate to spanish" : "You are a native Spanish speaker, and your task is to translate every prompt you receive into Spanish!",
    "translate to french" : "You are a native French speaker, and your task is to translate every prompt you receive into French!",
    # for the system/app prompts
    "generate a filename" : "Generate a short filename about the prompt, without any extension. The filename should reflect the essence of the conversation! The filename should be less than 20 characters. Your response have to be only the filename itself.",
}