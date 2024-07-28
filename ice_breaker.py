import os

from langchain.prompts.prompt import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.chains import LLMChain

from dotenv import load_dotenv
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties import linkedin


# information = """
# Ilaiyaraaja (born R. Gnanathesigan, 3 June 1943) is an Indian musician, composer, arranger, conductor, orchestrator, multi-instrumentalist, lyricist and playback singer popular for his works in Indian cinema, mainly in Tamil and Telugu films. Reputed to be one of the most prolific composer, in a career spanning over forty-eight years, he has composed over 7,000 songs and provided film scores for over 1,000 films,[1] apart from performing in over 20,000 concerts.[2] He is nicknamed "Isaignani" (the musical sage) and is often referred to as "Maestro", the title conferred to him by the Royal Philharmonic Orchestra, London.[3]

# Ilaiyaraaja was also one of the earliest Indian film composers to use Western classical music harmonies and string arrangements in Indian film music,[4] and the first South Asian to compose a full symphony.[5] In 1986, he became the first Indian composer to record a soundtrack with computer for the film Vikram.[6] He also composed Thiruvasagam in Symphony (2006), the first Indian oratorio.[7]

# In 2013, when CNN-IBN conducted a poll to commemorate 100 years of Indian cinema, he secured 49% of the vote and was adjudged the country's greatest music composer.[8] In 2014, the American world cinema portal "Taste of Cinema" placed him at 9th position in its list of 25 greatest film composers in the history of cinema. He is the only Indian in the list, appearing alongside Ennio Morricone, John Williams, and Jerry Goldsmith.[9][10]

# Ilaiyaraaja received several awards for his works throughout his career. In 2012, for his creative and experimental works in the field of music, he received the Sangeet Natak Akademi Award, the highest Indian recognition given to people in the field of performing arts. In 2010 he was awarded the Padma Bhushan, the third-highest civilian honour in India, and in 2018 was conferred with Padma Vibhushan, the second-highest civilian award by the government of India. He is a nominated Member of Parliament in the Indian upper house Rajya Sabha since July 2022.[11] A biographical film about his life titled "Ilaiyaraaja" was announced on 20 March 2024.
# """

def ice_break_with(name: str):
    linkedin_url = linkedin_lookup_agent(name)
    linkedin_profile_data = linkedin.scrape_linkedin_profile(linkedin_url)

    summary_template = """
        given the Linked information {information} about a person I want to create:
        1. a short summary
        2. two interesting facts about the person
    """

    summary_prompt_template = PromptTemplate(input_variables="information", template=summary_template)

    # llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    llm = ChatOllama(model="llama3")

    chain = summary_prompt_template | llm

    res = chain.invoke(input={"information": linkedin_profile_data})

    print(res)


if __name__ == '__main__':
    load_dotenv()
    print("Hello user, whom you want to ice break with:")
    user_input = input()
    ice_break_with("eden marco udemy")
