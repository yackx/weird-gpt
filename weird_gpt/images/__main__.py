from pathlib import Path

import openai


client = openai.OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    # api_key="My API Key",
)


def generate():
    response = client.images.generate(
        # prompt="A Magritte painting of a pipe with the caption 'Ceci n'est pas un budget participatif'.",
        # prompt="Two silhouettes laughing and chatting, one man one woman, stick figures.",
        prompt="""A surrealistic painting reminiscent of the early 20th-century Belgium art scene, 
        displaying a pipe and a blue euro currency sign intertwined with a yellow speech bubble, 
        with a written caption below it that reads 'Ceci n'est pas un budget participatif' verbatim 
        (please do not change the spelling). 
        The painting should be executed in the illusionistic, dream-like style typical of the pre-1912 surrealists, 
        using primarily oil as the medium.""",
        model="dall-e-3",
        n=1,
        quality="standard",
        response_format="url",
        style="natural",
        # size="512x512",
    )
    print(response)


def edit():
    response = client.images.edit(
        image=Path("/Users/youri/Downloads/budget_participatif_logo.png"),
        prompt="""A surrealistic painting reminiscent of the early 20th-century Belgium art scene,
        displaying a pipe with a written caption below it that reads 'Ceci n'est pas un budget participatif' verbatim.
        The painting should be executed in the illusionistic, dream-like style typical of the pre-1912 surrealists,
        using primarily oil as the medium. I should include the euro logo.""",
        # prompt="A Magritte painting with the caption 'Ceci n'est pas un budget participatif'.",
        n=1,
        response_format="url",
    )
    print(response)


if __name__ == "__main__":
    # edit()
    generate()
