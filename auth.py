from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def get_token_provider():
    """Initialize and return the Azure token provider."""
    return get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
