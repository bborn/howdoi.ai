"""Chain that calls GiphyAPi.
"""
import os
import sys
from typing import Any, Dict, Optional

# Use Pydantic v1 for LangChain compatibility if needed, or standard v2. 
# LangChain often re-exports v1. Let's use standard pydantic and rely on compatibility.
from pydantic import BaseModel, Field, model_validator

class HiddenPrints:
    """Context manager to hide prints."""

    def __enter__(self) -> None:
        """Open file to pipe stdout to."""
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, *_: Any) -> None:
        """Close file that stdout was piped to."""
        sys.stdout.close()
        sys.stdout = self._original_stdout


class GiphyAPIWrapper(BaseModel):
    """Wrapper around Giphy API."""

    giphy_api_key: Optional[str] = None
    giphy_engine: Any = None

    @model_validator(mode='before')
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        giphy_api_key = values.get("giphy_api_key") or os.environ.get("GIPHY_API_KEY")
        values["giphy_api_key"] = giphy_api_key
        
        try:
            import giphy_client
            from giphy_client.rest import ApiException

            values["giphy_engine"] = giphy_client.DefaultApi()
        except ImportError:
            raise ValueError(
                "Could not import giphy_client python package. "
                "Please it install it with `pip install giphy_client`."
            )
        return values

    def run(self, query: str) -> str:
        """Run query through GiphyAPI and parse result."""
        api_key = self.giphy_api_key
        q = query
        limit = 5
        offset = 0
        rating = 'g'
        lang = 'en'
        fmt = 'json'

        if not self.giphy_engine:
             import giphy_client
             self.giphy_engine = giphy_client.DefaultApi()

        with HiddenPrints():
            try:
                # Search Endpoint
                api_response = self.giphy_engine.gifs_search_get(
                    api_key, q, limit=limit, offset=offset, rating=rating, lang=lang, fmt=fmt)
            except Exception as e:
                # Return an error message instead of crashing
                return f"Error fetching Giphy: {str(e)}"

        if not api_response.data:
            return "No matching gif found."

        url = api_response.data[0].embed_url

        return f"""<iframe src="{url}" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><br /><a href="{url}">powered by GIPHY</a>"""