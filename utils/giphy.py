"""Chain that calls GiphyAPi.

"""
import os
import sys
from typing import Any, Dict, Optional

from pydantic import BaseModel, Extra, root_validator

from langchain.utils import get_from_dict_or_env


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
    """Wrapper around Giphy API.

    To use, you should have the environment variable ``GIPHY_API_KEY`` set with your API key, or pass
    `giphyapi_api_key` as a named parameter to the constructor.

    Example:
        .. code-block:: python

            from langchain import SerpAPIWrapper
            serpapi = SerpAPIWrapper()
    """

    search_engine: Any  #: :meta private:

    giphy_api_key: Optional[str] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        giphy_api_key = get_from_dict_or_env(
            values, "giphy_api_key", "GIPHY_API_KEY"
        )
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
        api_key = self.giphy_api_key  # str | Giphy API Key.
        q = query  # str | Search query term or prhase.
        # int | The maximum number of records to return. (optional) (default to 25)
        limit = 5
        # int | An optional results offset. Defaults to 0. (optional) (default to 0)
        offset = 0
        rating = 'g'  # str | Filters results by specified rating. (optional)
        # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
        lang = 'en'
        fmt = 'json'  # str | U

        with HiddenPrints():
            try:
                # Search Endpoint
                api_response = self.giphy_engine.gifs_search_get(
                    api_key, q, limit=limit, offset=offset, rating=rating, lang=lang, fmt=fmt)
            except ApiException as e:
                raise ValueError(f"Got error from GiphyAPI: {e}")

        # raise Exception(api_response.data[0].embed_url)
        url = api_response.data[0].embed_url

        return f"""<iframe src="{url}" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><br /><a href="{url}">powered by GIPHY</a>"""
