from semantic_router import Route,SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.index import LocalIndex

index=LocalIndex()
from semantic_router.encoders import FastEmbedEncoder

# encoder = FastEmbedEncoder(model_name="BAAI/bge-large-en-v1.5")
encoder=HuggingFaceEncoder(name='intfloat/e5-base-v2')


faq = Route(
    name='faq',
    utterances=[
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
    ]
)

sql = Route(
    name='sql',
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
    ]
)
gibberies = Route(
    name='gibberies',
    utterances=[
        "cccccc",
        "vvvvcccccc",
        "gfbhn vcv vcv ",
        "gbg",
        " ",
    ]
)

router=SemanticRouter(encoder=encoder,routes=[faq,sql,gibberies],index=index)
router.sync(sync_mode='local')
if __name__ == "__main__":
    print(router( "How can I track my order?").name)
    print(router("Pink Puma shoes in price range 500 to 1000").name)
    print(router("inknjj").name)