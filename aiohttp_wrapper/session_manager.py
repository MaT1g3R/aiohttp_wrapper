from http import HTTPStatus
from io import BytesIO
from json import loads
from typing import Optional, Tuple

from aiohttp import ClientResponse, ClientSession
from xmltodict import parse

from .errors import HTTPStatusError


class SessionManager:
    """
    An aiohttp client session manager.
    """
    __slots__ = ('session', 'codes')

    def __init__(self):
        """
        Initialize the instance of this class.
        """
        self.session = None
        self.codes = {l.value: l.description for l in list(HTTPStatus)}

    async def get(self, url, range_: Tuple[int, int] = (200, 299), *,
                  allow_redirects=True, **kwargs) -> ClientResponse:
        """
        Make HTTP GET request

        :param url: Request URL, str or URL

        :param range_:
            the accepted range for status code, inclusive.
            defaults to 200-299

        :param allow_redirects: If set to False, do not follow redirects.
        True by default (optional).

        :param kwargs: In order to modify inner request parameters,
        provide kwargs.

        :return: a client response object.

        :raises: HTTPStatusError if status code isn't in the range.
        """
        session = await self.__session()
        r = await session.get(url, allow_redirects=allow_redirects, **kwargs)
        return await self.__return_response(r, r.status, range_)

    async def post(self, url, range_: Tuple[int, int] = (200, 299), *,
                   data=None, **kwargs) -> ClientResponse:
        """
        Make HTTP POST request.

        :param url: Request URL, str or URL

        :param range_:
            the accepted range for status code, inclusive.
            defaults to 200-299

        :param data: Dictionary, bytes, or file-like object to send in the
        body of the request (optional)

        :param kwargs: In order to modify inner request parameters,
        provide kwargs.

        :return: a client response object.

        :raises: HTTPStatusError if status code isn't in the range.
        """
        session = await self.__session()
        resp = await session.post(url, data=data, **kwargs)
        return await self.__return_response(resp, resp.status, range_)

    async def get_json(self, url, params: dict = None,
                       range_: Tuple[int, int] = (200, 299), **kwargs):
        """
        Return the json content from an HTTP request using Aiohttp.

        :param url: the url.

        :param params: the request params.

        :param range_:
            the accepted range for status code, inclusive.
            defaults to 200-299

        :return: the json content in a python dict.

        :raises HTTPStatusError: if the status code isn't in the range.
        """
        async with await self.get(url, range_, params=params, **kwargs) as r:
            content = await r.read()
            return loads(content) if content else None

    async def get_xml(
            self, url, params: dict = None,
            range_: Tuple[int, int] = (200, 299), **kwargs) -> Optional[dict]:
        """
        Return the xml content from an HTTP request using Aiohttp.

        :param url: the url.

        :param params: the request params.

        :param range_:
            the accepted range for status code, inclusive.
            defaults to 200-299

        :return: the xml content in a python dict.

        :raises HTTPStatusError: if the status code isn't in the range.
        """
        async with await self.get(url, range_, params=params, **kwargs) as r:
            content = await r.read()
            return parse(content) if content else None

    async def bytes_io(self, url,
                       range_: Tuple[int, int] = (200, 299)) -> BytesIO:
        """
        Convert an url content to BytesIO

        :param url: the url.

        :param range_:
            the accepted range for status code, inclusive.
            defaults to 200-299

        :return: a BytesIO object from the get request of the url.

        :raises: HTTPStatusError if status code isn't in the range.
        """
        async with await self.get(url, range_) as resp:
            content = await resp.read()
            return BytesIO(content)

    async def __session(self):
        if not self.session:
            self.session = ClientSession()
        return self.session

    async def __return_response(self, res, code, range_):
        """
        Return an Aiohttp or Request response object.
        :param res: the response.
        :param code: the response code.
        :return: the response object.
        :raises: HTTPStatusError if status code isn't 200
        """
        low, high = range_
        if low <= code <= high:
            return res
        else:
            async with res:
                raise HTTPStatusError(code, self.codes.get(code, None))

    def __del__(self):
        """
        Class destructor, close the client session.
        """
        if self.session:
            self.session.close()
