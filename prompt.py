ANSWERING_PROMPT = "You are tasked with answering the user\'s question as accurately and reasonably as possible.\n\
        You must provide both the answer and the reasoning behind your answer in a clear and structured manner.\n\
        Another LLM will attempt to refute your response, so ensure that your reasoning is logical and well-supported \
        with facts, evidence, or clear principles.\nBe ready to provide clarification if necessary. The question of user:\n"

QUESTION_PROMPT = "Your role is to critically evaluate the previous response.\n\
        You will attempt to refute it by pointing out any inconsistencies, gaps\n\
        in reasoning, or alternative interpretations that could challenge the answer.\n\
        Focus on finding potential weaknesses in logic or factual errors.\n\
        However, if the answer provided is sufficiently reasonable and you agree with the reasoning,\n\
        you must acknowledge that and say OK.\n\
         Your goal is to push the other LLM to improve its reasoning, but also to accept when a conclusion is well-supported."

SUMMARY_PROMPT = "You will be given a history of an adversarial exchange between two LLMs,\n\
        one answering a question and the other refuting the answer. Your task is to summarize\n\
        the outcome of this exchange, focusing on the key points raised by both sides.\n\
        Consider:\n\
	1.What was the original answer?\n\
	2.What arguments did the refuting LLM present against the answer?\n\
	3.How did the answering LLM respond to the refutations?\n\
	4.Did both LLMs reach a reasonable conclusion that they agree on? If so, what is it?\n\
        Summarize the key insights from the exchange, highlighting both the strengths and weaknesses of the arguments,\n\
        and explain the final conclusion that emerged from the dialogue."