from utils.completion import openai_completion
from utils.notes import process_notes, choose_random_note

def main():    
    print("Hello world")

    # Generate ideas to write about
    ideas_prompt = [
        {"role": "user", "content": f"""**Task**
        Please generated a numbered list of 10 topics that we could write a short essay about. 
        Some topics I'm interested in are: economics, history, space, physics,
        affordable housing, the Bible, religion, immigration, tax policy, 
        emerging technology, the impact of technology on society, and more. 

        The essay topics should be interesting to me. 
        The essay topics should also be something that the some of the following writers might write about:
        Matthew Yglesias, Noah Smith, Hannah Ritchie, Andre Perry, Derek Thompson

        Please respond only with the list and nothing else.
        """}
    ]

    print("\nGenerating essay ideas...\n")
    response = openai_completion(ideas_prompt, temperature=1)
    ideas = response['choices'][0]['message']['content']
    print(ideas)


    # Write a short essay on the topic
    # Trying this with keeping the ideas prompt in there as context -- nevermind it kind of anchors to the writers in an annoying way
    essay_prompt = [{"role": "user", "content": f"""**Task**
        Below is a list of essay topics
        Please choose one topic AT RANDOM and draft a short, high-quality article on the topic. 
        The article should be concise -- avoid filler words. 
        Be creative! This is just a first draft.
        Here are the potential topics: {ideas}
    """}]

    print("\nChoosing an idea and writing an essay...\n")
    response = openai_completion(essay_prompt, temperature=0.7)
    essay = response['choices'][0]['message']['content']
    print(essay)

    # Chunk the writing into core ideas and create "evergreen notes"
    notes_prompt = [
         {"role": "user", "content": f"""**Task**
         Another agent has generated an essay. 
         Your job is to use the essay as inspiration to write some Evergreen Notes on that topic or similar topics. 
         You should use the most interesting ideas from the essay but you can also bring in new ideas. 
         """},

         {"role": "user", "content": f"""**What are Evergreen Notes?**
         Evergreen Notes have the following properties:
            1. Evergreen Notes consist of a bolded title and the text of the note
            2. Evergreen Notes should be atomic. It’s best to create notes which are only about one thing—but which, as much as possible, capture the entirety of that thing.
            3. Evergreen Notes should be concept-oriented. It’s best to factor Evergreen notes by concept (rather than by author, book, event, project, topic, etc). This way, you discover connections across books and domains as you update and link to the note over time 
            4. Evergreen Notes should be densely-linked.  If we push ourselves to add lots of links between our notes, that makes us think expansively about what other concepts might be related to what we’re thinking about. It creates pressure to think carefully about how ideas relate to each other 
            5. Evergreen Notes can link to other Notes through the title in this format: [[Title]]
            6. Evergreen Note titles are like APIs. When Evergreen notes are factored and titled well, those titles become an abstraction for the note itself. The entire note’s ideas can then be referenced using that handle. In fact, this property itself functions as a kind of litmus: as you develops ideas in notes over time and improve the “APIs,” you’ll be able to write individual notes which abstract over increasingly large subtrees. 
         """},

         {"role": "user", "content": f"""**Examples of Evergreen Notes**
         Here are 3 examples of good Evergreen Notes on a totally unrelated topic

            **Write notes for yourself by default, disregarding audience**
            Because Evergreen notes can be used as part of a strategy for writing public work ([[Executable strategy for writing]]), it’s tempting to “save time” by writing notes in publishable form. That might mean providing all the necessary background to understand some (boring to you) idea, or self-censoring, or adding lots of qualifiers, or spending lots of effort on clarity. Many of these practices can be somewhat useful as part of your own thinking process—for instance, clearer writing usually involves clearer thinking. But I find it substantially increases the overhead and effort in writing, often to the point of producing blockage.

            More concretely, this manifests as a common failure mode for me when I’m writing notes as part of explicit preparation for some public writing. I’ll often try to do both jobs at once. That is, I might be writing atomic-style notes ([[Evergreen notes should be atomic]]) but I try to write them as if they’re sections in a larger essay or work. Or even just: I try to write things with all the context and clear prose needed for an outsider to understand what I’m talking about. Then I often find that I can’t write anything at all! Better to write at a level where I can produce something, then use that to lever myself upward. ([[Evergreen notes permit smooth incremental progress in writing (“incremental writing”)]])


            **Knowledge work requires good writing**
            Every job I’ve had so far involves writing. Why didn’t anybody tell me this in school? Maybe I wasn’t paying attention. I write memos, slide decks, emails, assignments, applications… [[Amazon made famous a “six page memo” format for business writing]]

            Quality of writing in the workplace seems to matter: bad writing leads to miscommunication, churn, or tossed projects. Good writing leads to new opportunities, greenlit projects, and promotions. 

            Also, compared to other skills writing may be a bigger differentiator, because lots of people do not practice writing. So being able to write quickly, with concision, and with understanding is a competitive advantage. [[If AI makes work more bimodal - I want to be the top bucket]]

            Now this might be changing with generative AI in writing. What happens when everyone is having a LLM generate the polite, cogent, and short email? 

            Even still, being able clearly communicate what you need in a couple bullet points without being a jerk will remain helpful. And that’s still good writing!

            **Avoiding the feeling of busyness can probably lead to stronger prioritization towards impact**
            Vibes of busyness lead to poor decision making in business. This is because lots of people have a reflex to push away new work when they're feeling busy, at least in my experience... but that can lead to seeing trees and not forest. The result is that you don't start something that is important, important enough that with more space to think you probably would take that work up, even if it requires dropping something else. 

         """},

        {"role": "user", "content": f"**Essay from another agent**\n{essay}"},

        {"role": "user", "content": f"""**Agent Response**
                Use the essay as inspiration to write some Evergreen Notes formatted per the above properties.
                Respond only with the Notes.
                Keep in mind the correct formatting of notes: bold titles followed by a paragraph of text. 
                Titles should NOT say "evergreen note" in them. Simply the title that summarizes the note.""" }
        ]
    
    print("\nForming some notes...\n")
    response = openai_completion(notes_prompt)
    notes = response['choices'][0]['message']['content']
    print(notes)

    # Critique , edit, and save just a couple evergreen notes
    edits_prompt = [
        {"role": "system", "content": "You are a helpful assistant. You can only respond with an array that can be used in Python."},

        {"role": "user", "content": f"""**Task**
         Another agent has generated these basic Evergreen Notes. 
         Your job is to select the best notes, significantly expand and improve them, and then save only the best of these Evergreen Notes. 
         """},
        
        {"role": "user", "content": f"""**What are Evergreen Notes?**
         Evergreen Notes have the following properties:
            1. Evergreen Notes consist of a bolded title and the text of the note
            2. Evergreen Notes should be atomic. It’s best to create notes which are only about one thing—but which, as much as possible, capture the entirety of that thing.
            3. Evergreen Notes should be concept-oriented. It’s best to factor Evergreen notes by concept (rather than by author, book, event, project, topic, etc). This way, you discover connections across books and domains as you update and link to the note over time 
            4. Evergreen Notes should be densely-linked.  If we push ourselves to add lots of links between our notes, that makes us think expansively about what other concepts might be related to what we’re thinking about. It creates pressure to think carefully about how ideas relate to each other 
            5. Evergreen Notes can link to other Notes through the title in this format: [[Title]]
            6. Evergreen Note titles are like APIs. When Evergreen notes are factored and titled well, those titles become an abstraction for the note itself. The entire note’s ideas can then be referenced using that handle. In fact, this property itself functions as a kind of litmus: as you develops ideas in notes over time and improve the “APIs,” you’ll be able to write individual notes which abstract over increasingly large subtrees. 
            7. Titles that are complete phrases are preferred to maintain concept-orientation. For example: [[Educational objectives often subvert themselves]], [[Evergreen notes permit smooth incremental progress in writing (“incremental writing”)]] are much better titles than [[Educational objectives]] 
                Titles are often declarative or imperative phrases making a strong claim. This puts pressure on me to adequately support the claim in the body. If I write a note but struggle to summarize it in a sharp title, that’s often a sign that my thinking is muddy or that this note is about several topics (contra Evergreen notes should be atomic). In both cases, the solution is to break the ideas down and write about the bits I understand best first.
                Questions also make good note titles because that position creates pressure to make the question get to the core of the matter. 
         """},

        {"role": "user", "content": f"**Notes from another agent**\n{notes}"},

        {"role": "user", "content": f"""**Agent Response**
            Select, improve, and expand at most 3 notes from the above list, based on your judgement as to which are the best
            and most likely to be useful in other contexts.

            Good notes are at least a paragraph or two. 
            
            Your response MUST be formatted as a nested array in the following format so that it can be used in Python:
            [["title", "note"], ["title", "note"]]""" }
    ]

    print("\nEditing these notes...\n")
    response = openai_completion(edits_prompt, temperature=0.2)
    notes = response['choices'][0]['message']['content']
    
    # Parse the array and save the notes as .txt files to /notes
    #print(notes)
    process_notes(notes)

    # Go through the notes and make connections
    for i in range(10):
        j = i+1
        # Choose a note at random, get the title, text, and list of other titles
        title, text, other_notes = choose_random_note()

        # Prompt to edit that specific note to make connections
        connections_prompt = [
            {"role": "system", "content": "You are a helpful assistant. You can only respond with an array that can be used in Python."},

            {"role": "user", "content": f"""**Task**
            The user has selected an Evergreen Note. 
            Your job is to make RELEVANT, IN-LINE connections from the Selected Note to some of the other available notes. 
            """},

            {"role": "user", "content": f"""**What are Evergreen Notes?**
            Evergreen Notes have the following properties:
                1. Evergreen Notes consist of a bolded title and the text of the note
                2. Evergreen Notes should be atomic. It’s best to create notes which are only about one thing—but which, as much as possible, capture the entirety of that thing.
                3. Evergreen Notes should be concept-oriented. It’s best to factor Evergreen notes by concept (rather than by author, book, event, project, topic, etc). This way, you discover connections across books and domains as you update and link to the note over time 
                4. Evergreen Notes should be densely-linked.  If we push ourselves to add lots of links between our notes, that makes us think expansively about what other concepts might be related to what we’re thinking about. It creates pressure to think carefully about how ideas relate to each other 
                5. IMPORTANT: Evergreen Notes can link to other Notes through the title in this format: [[Title]]
                6. Evergreen Note titles are like APIs. When Evergreen notes are factored and titled well, those titles become an abstraction for the note itself. The entire note’s ideas can then be referenced using that handle. In fact, this property itself functions as a kind of litmus: as you develops ideas in notes over time and improve the “APIs,” you’ll be able to write individual notes which abstract over increasingly large subtrees. 
                7. Titles that are complete phrases are preferred to maintain concept-orientation. For example: [[Educational objectives often subvert themselves]], [[Evergreen notes permit smooth incremental progress in writing (“incremental writing”)]] are much better titles than [[Educational objectives]] 
                    Titles are often declarative or imperative phrases making a strong claim. This puts pressure on me to adequately support the claim in the body. If I write a note but struggle to summarize it in a sharp title, that’s often a sign that my thinking is muddy or that this note is about several topics (contra Evergreen notes should be atomic). In both cases, the solution is to break the ideas down and write about the bits I understand best first.
                    Questions also make good note titles because that position creates pressure to make the question get to the core of the matter. 
            """},

            {"role": "user", "content": f"**The Selected Note**\n{title}\n{text}"},
            {"role": "user", "content": f"**Titles of other available notes**\n{other_notes}"},

            {"role": "user", "content": f"""**Agent Response**
            Take the Selected Note and edit it. 
            Your goal is to add RELEVANT connections to the Selected Note. 
            Do not add connections that are not RELEVANT IN-LINE

            Make connections by referencing other titles in the middle of the note text with double square brackets, like this: [[title]]
            Always use [[]] to reference other notes

            If there are no RELEVANT connections to add then that is OK.
            You may also edit the text of the Selected Note if it can be improved at this time. 
            
            Your final response MUST be formatted as a nested array consisting of the updated Selected Note that you have edited in the following format so that it can be used in Python:
            [["title", "note"]]"""}
        ]

        # TODO: Add function call option (but gets lotsa more expensive)

        print(f"\nMaking connections between notes... {j}\n")
        print("FROM:")
        print(title)
        print(text)
        response = openai_completion(connections_prompt, temperature=0.2)
        notes = response['choices'][0]['message']['content']
        print("TO:")
        process_notes(notes)


if __name__ == "__main__":
    main()
