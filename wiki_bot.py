import wikipedia

def get_wiki_answer(query):

    try:
        # Step 1: search best matching title
        search_results = wikipedia.search(query)

        if not search_results:
            return "Sorry, I couldn't find anything about that."

        best_match = search_results[0]

        # Step 2: get summary
        summary = wikipedia.summary(best_match, sentences=4)

        return f"{best_match}\n\n{summary}"

    except wikipedia.exceptions.DisambiguationError as e:
        # pick first option automatically (smarter behavior)
        option = e.options[0]
        summary = wikipedia.summary(option, sentences=4)
        return summary

    except Exception:
        return "I couldn't fetch information right now."