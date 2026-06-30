import litellm
import logging
import os

from litellm.exceptions import AuthenticationError, RateLimitError, BadRequestError

logger = logging.getLogger(__name__)

class AIHandler:
    def __init__(self, config):
        self.config = config
        self.ai_settings = getattr(self.config, "ai", {})
        self.model = self.ai_settings.get("model")
        self.api_key = self._get_api_key()
        self._validate_self()

        logger.info(f"Using api_key: {self.api_key[0:15]}...")

    def _get_api_key(self):
        LIFELOG_LLM_API_KEY = os.getenv("LIFELOG_LLM_API_KEY")
        if LIFELOG_LLM_API_KEY:
            return LIFELOG_LLM_API_KEY
        else:
            self.ai_settings.get("api_key")

    def _validate_self(self):
        if not self.api_key: 
            msg = "Api key is missing in the config."
            logger.error(msg)
            raise ValueError(msg)
        
        if not self.model:
            logger.error("No model specified in config.")
            raise ValueError(msg)

    def send_prompt(self, messages):
        try:
            response = litellm.completion(
                model=self.model,
                messages=messages,
                api_key=self.api_key,
                num_retries=2 
            )
            return response

        except AuthenticationError:
            logger.error(f"Authentication failed. Check your API key for {self.model}.")
        except RateLimitError:
            logger.error(f"Rate limit exceeded for {self.model}. Try again later.")
        except BadRequestError as e:
            logger.error(f"Invalid request sent to provider: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred in AIHandler: {e}")
            
        return None

    # remove?
    def get_content(self, messages):
        response = self.send_prompt(messages)
        if response:
            return response.choices[0].message.content
        return ""
