from openai import OpenAI

client = OpenAI()


def moderate(message):
    return client.moderations.create(input=message)


def moderate_aggregate(message) -> dict[str, float] | bool:
    moderation = moderate(message)
    result = moderation.results[0]
    flagged = result.flagged
    if flagged:
        flagged_categories = [
            k for k, v in result.categories.model_extra.items() if v is True
        ]
        category_scores = {
            k: v
            for k, v in result.category_scores.model_extra.items()
            if k in flagged_categories
        }
        return category_scores
    else:
        return False
