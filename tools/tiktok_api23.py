#!/usr/bin/env python3
"""
TikTok API23 - Cliente Python para RapidAPI
38 endpoints completos: User, Search, Post, Trending, Challenge, Place

Autor: Felipe M. de Paula
Data: 2025-11-02
"""

import http.client
import json
import sys
import time
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode

# Adicionar diretório config ao path
sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace')
from config.tiktok_config import RAPIDAPI_HOST, HEADERS, DEFAULT_COUNT, DEFAULT_CURSOR, MAX_RETRIES, TIMEOUT


class TikTokAPI23:
    """Cliente para TikTok API23 (RapidAPI)"""

    def __init__(self):
        self.host = RAPIDAPI_HOST
        self.headers = HEADERS
        self.max_retries = MAX_RETRIES
        self.timeout = TIMEOUT

    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """
        Faz requisição HTTP à API

        Args:
            endpoint: Endpoint completo (ex: /api/user/info?uniqueId=taylorswift)

        Returns:
            Dict com resposta da API
        """
        for attempt in range(self.max_retries):
            try:
                conn = http.client.HTTPSConnection(self.host, timeout=self.timeout)
                conn.request("GET", endpoint, headers=self.headers)

                res = conn.getresponse()
                data = res.read()
                conn.close()

                # Parse JSON
                return json.loads(data.decode("utf-8"))

            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Erro após {self.max_retries} tentativas: {str(e)}")
                time.sleep(1)  # Aguarda 1s antes de retry

    # ==========================================
    # USER ENDPOINTS (12)
    # ==========================================

    def get_user_info(self, unique_id: str) -> Dict[str, Any]:
        """
        Obter informações de usuário por @username

        Args:
            unique_id: Username do TikTok (ex: taylorswift)
        """
        endpoint = f"/api/user/info?uniqueId={unique_id}"
        return self._make_request(endpoint)

    def get_user_info_with_region(self, unique_id: str) -> Dict[str, Any]:
        """
        Obter informações de usuário com dados de região

        Args:
            unique_id: Username do TikTok
        """
        endpoint = f"/api/user/info-with-region?uniqueId={unique_id}"
        return self._make_request(endpoint)

    def get_user_info_by_id(self, user_id: str) -> Dict[str, Any]:
        """
        Obter informações de usuário por ID numérico

        Args:
            user_id: ID numérico do usuário
        """
        endpoint = f"/api/user/info-by-id?userId={user_id}"
        return self._make_request(endpoint)

    def get_user_followers(self, sec_uid: str, count: int = DEFAULT_COUNT,
                          min_cursor: int = DEFAULT_CURSOR) -> Dict[str, Any]:
        """
        Obter lista de seguidores de um usuário

        Args:
            sec_uid: ID seguro do usuário
            count: Quantidade de resultados (padrão: 30)
            min_cursor: Cursor para paginação (padrão: 0)
        """
        endpoint = f"/api/user/followers?secUid={sec_uid}&count={count}&minCursor={min_cursor}"
        return self._make_request(endpoint)

    def get_user_followings(self, sec_uid: str, count: int = DEFAULT_COUNT,
                           min_cursor: int = DEFAULT_CURSOR,
                           max_cursor: int = DEFAULT_CURSOR) -> Dict[str, Any]:
        """
        Obter lista de quem o usuário segue

        Args:
            sec_uid: ID seguro do usuário
            count: Quantidade de resultados
            min_cursor: Cursor mínimo
            max_cursor: Cursor máximo
        """
        endpoint = f"/api/user/followings?secUid={sec_uid}&count={count}&minCursor={min_cursor}&maxCursor={max_cursor}"
        return self._make_request(endpoint)

    def get_user_popular_posts(self, sec_uid: str, count: int = 35,
                              cursor: int = DEFAULT_CURSOR) -> Dict[str, Any]:
        """
        Obter posts mais populares do usuário

        Args:
            sec_uid: ID seguro do usuário
            count: Quantidade de posts
            cursor: Cursor para paginação
        """
        endpoint = f"/api/user/popular-posts?secUid={sec_uid}&count={count}&cursor={cursor}"
        return self._make_request(endpoint)

    def get_user_oldest_posts(self, sec_uid: str, count: int = DEFAULT_COUNT,
                             cursor: int = DEFAULT_CURSOR) -> Dict[str, Any]:
        """
        Obter posts mais antigos do usuário

        Args:
            sec_uid: ID seguro do usuário
            count: Quantidade de posts
            cursor: Cursor para paginação
        """
        endpoint = f"/api/user/oldest-posts?secUid={sec_uid}&count={count}&cursor={cursor}"
        return self._make_request(endpoint)

    def get_user_liked_posts(self, sec_uid: str, count: int = DEFAULT_COUNT,
                            cursor: int = DEFAULT_CURSOR) -> Dict[str, Any]:
        """
        Obter posts curtidos pelo usuário

        Args:
            sec_uid: ID seguro do usuário
            count: Quantidade de posts
            cursor: Cursor para paginação
        """
        endpoint = f"/api/user/liked-posts?secUid={sec_uid}&count={count}&cursor={cursor}"
        return self._make_request(endpoint)

    def get_user_playlist(self, sec_uid: str, count: int = 20,
                         cursor: int = DEFAULT_CURSOR) -> Dict[str, Any]:
        """
        Obter playlists do usuário

        Args:
            sec_uid: ID seguro do usuário
            count: Quantidade de playlists
            cursor: Cursor para paginação
        """
        endpoint = f"/api/user/playlist?secUid={sec_uid}&count={count}&cursor={cursor}"
        return self._make_request(endpoint)

    def get_user_repost(self, sec_uid: str, count: int = DEFAULT_COUNT,
                       cursor: int = DEFAULT_CURSOR) -> Dict[str, Any]:
        """
        Obter reposts do usuário

        Args:
            sec_uid: ID seguro do usuário
            count: Quantidade de reposts
            cursor: Cursor para paginação
        """
        endpoint = f"/api/user/repost?secUid={sec_uid}&count={count}&cursor={cursor}"
        return self._make_request(endpoint)

    def get_user_story(self, user_id: str, max_cursor: int = DEFAULT_CURSOR) -> Dict[str, Any]:
        """
        Obter stories do usuário

        Args:
            user_id: ID numérico do usuário
            max_cursor: Cursor máximo para paginação
        """
        endpoint = f"/api/user/story?userId={user_id}&maxCursor={max_cursor}"
        return self._make_request(endpoint)

    # ==========================================
    # SEARCH ENDPOINTS (4)
    # ==========================================

    def search_general(self, keyword: str, cursor: int = DEFAULT_CURSOR,
                      search_id: int = 0) -> Dict[str, Any]:
        """
        Busca geral no TikTok

        Args:
            keyword: Termo de busca
            cursor: Cursor para paginação
            search_id: ID da busca (padrão: 0)
        """
        endpoint = f"/api/search/general?keyword={keyword}&cursor={cursor}&search_id={search_id}"
        return self._make_request(endpoint)

    def search_videos(self, keyword: str, cursor: int = DEFAULT_CURSOR,
                     search_id: int = 0) -> Dict[str, Any]:
        """
        Buscar vídeos específicos

        Args:
            keyword: Termo de busca
            cursor: Cursor para paginação
            search_id: ID da busca
        """
        endpoint = f"/api/search/video?keyword={keyword}&cursor={cursor}&search_id={search_id}"
        return self._make_request(endpoint)

    def search_accounts(self, keyword: str, cursor: int = DEFAULT_CURSOR,
                       search_id: int = 0) -> Dict[str, Any]:
        """
        Buscar contas/usuários

        Args:
            keyword: Termo de busca
            cursor: Cursor para paginação
            search_id: ID da busca
        """
        endpoint = f"/api/search/account?keyword={keyword}&cursor={cursor}&search_id={search_id}"
        return self._make_request(endpoint)

    def search_others_searched_for(self, keyword: str) -> Dict[str, Any]:
        """
        Obter sugestões de busca relacionadas

        Args:
            keyword: Termo de busca
        """
        endpoint = f"/api/search/others-searched-for?keyword={keyword}"
        return self._make_request(endpoint)

    # ==========================================
    # POST (VIDEO) ENDPOINTS (5)
    # ==========================================

    def get_post_detail(self, video_id: str) -> Dict[str, Any]:
        """
        Obter detalhes completos de um vídeo

        Args:
            video_id: ID do vídeo
        """
        endpoint = f"/api/post/detail?videoId={video_id}"
        return self._make_request(endpoint)

    def get_post_comments(self, video_id: str, count: int = 50,
                         cursor: int = DEFAULT_CURSOR) -> Dict[str, Any]:
        """
        Obter comentários de um vídeo

        Args:
            video_id: ID do vídeo
            count: Quantidade de comentários
            cursor: Cursor para paginação
        """
        endpoint = f"/api/post/comments?videoId={video_id}&count={count}&cursor={cursor}"
        return self._make_request(endpoint)

    def get_comment_replies(self, video_id: str, comment_id: str,
                           count: int = 6, cursor: int = DEFAULT_CURSOR) -> Dict[str, Any]:
        """
        Obter respostas de um comentário

        Args:
            video_id: ID do vídeo
            comment_id: ID do comentário
            count: Quantidade de respostas
            cursor: Cursor para paginação
        """
        endpoint = f"/api/post/comment/replies?videoId={video_id}&commentId={comment_id}&count={count}&cursor={cursor}"
        return self._make_request(endpoint)

    def get_trending_posts(self, count: int = 16) -> Dict[str, Any]:
        """
        Obter vídeos em alta/trending

        Args:
            count: Quantidade de vídeos
        """
        endpoint = f"/api/post/trending?count={count}"
        return self._make_request(endpoint)

    def explore_posts(self, category_type: int = 119, count: int = 16) -> Dict[str, Any]:
        """
        Explorar posts por categoria

        Args:
            category_type: Tipo de categoria (padrão: 119)
            count: Quantidade de posts
        """
        endpoint = f"/api/post/explore?categoryType={category_type}&count={count}"
        return self._make_request(endpoint)

    # ==========================================
    # TRENDING/ADS ENDPOINTS (13)
    # ==========================================

    def get_trending_ads_detail(self, ads_id: str) -> Dict[str, Any]:
        """
        Obter detalhes de um anúncio em trending

        Args:
            ads_id: ID do anúncio
        """
        endpoint = f"/api/trending/ads/detail?ads_id={ads_id}"
        return self._make_request(endpoint)

    def get_trending_ads(self, page: int = 1, period: int = 7, limit: int = 20,
                        country: str = "US", order_by: str = "ctr") -> Dict[str, Any]:
        """
        Obter anúncios em alta

        Args:
            page: Número da página
            period: Período em dias
            limit: Limite de resultados
            country: Código do país (padrão: US)
            order_by: Ordenar por (ctr, impressions, etc)
        """
        endpoint = f"/api/trending/ads?page={page}&period={period}&limit={limit}&country={country}&order_by={order_by}"
        return self._make_request(endpoint)

    def get_trending_creators(self, page: int = 1, limit: int = 20,
                             sort_by: str = "follower", country: str = "US") -> Dict[str, Any]:
        """
        Obter criadores em alta

        Args:
            page: Número da página
            limit: Limite de resultados
            sort_by: Ordenar por (follower, engagement, etc)
            country: Código do país
        """
        endpoint = f"/api/trending/creator?page={page}&limit={limit}&sort_by={sort_by}&country={country}"
        return self._make_request(endpoint)

    def get_trending_hashtags(self, page: int = 1, limit: int = 20, period: int = 120,
                             country: str = "US", sort_by: str = "popular") -> Dict[str, Any]:
        """
        Obter hashtags em alta

        Args:
            page: Número da página
            limit: Limite de resultados
            period: Período em horas
            country: Código do país
            sort_by: Ordenar por (popular, trending, etc)
        """
        endpoint = f"/api/trending/hashtag?page={page}&limit={limit}&period={period}&country={country}&sort_by={sort_by}"
        return self._make_request(endpoint)

    def get_trending_songs(self, page: int = 1, limit: int = 20, period: int = 7,
                          rank_type: str = "popular", country: str = "US") -> Dict[str, Any]:
        """
        Obter músicas em alta

        Args:
            page: Número da página
            limit: Limite de resultados
            period: Período em dias
            rank_type: Tipo de ranking (popular, trending)
            country: Código do país
        """
        endpoint = f"/api/trending/song?page={page}&limit={limit}&period={period}&rank_type={rank_type}&country={country}"
        return self._make_request(endpoint)

    def get_trending_keywords(self, page: int = 1, limit: int = 20,
                             period: int = 7, country: str = "US") -> Dict[str, Any]:
        """
        Obter keywords em alta

        Args:
            page: Número da página
            limit: Limite de resultados
            period: Período em dias
            country: Código do país
        """
        endpoint = f"/api/trending/keyword?page={page}&limit={limit}&period={period}&country={country}"
        return self._make_request(endpoint)

    def get_commercial_music_playlist_detail(self, playlist_id: str, page: int = 1,
                                            limit: int = 20, region: str = "US") -> Dict[str, Any]:
        """
        Obter detalhes de playlist da biblioteca comercial de música

        Args:
            playlist_id: ID da playlist
            page: Número da página
            limit: Limite de resultados
            region: Região (padrão: US)
        """
        endpoint = f"/api/trending/commercial-music-library/playlist/detail?playlist_id={playlist_id}&page={page}&limit={limit}&region={region}"
        return self._make_request(endpoint)

    def get_commercial_music_playlists(self, limit: int = 20, region: str = "US") -> Dict[str, Any]:
        """
        Obter playlists da biblioteca comercial de música

        Args:
            limit: Limite de resultados
            region: Região
        """
        endpoint = f"/api/trending/commercial-music-library/playlist?limit={limit}&region={region}"
        return self._make_request(endpoint)

    def get_commercial_music_library(self, page: int = 1, limit: int = 20,
                                    region: str = "US", scenarios: int = 0,
                                    duration: int = 0) -> Dict[str, Any]:
        """
        Obter músicas da biblioteca comercial

        Args:
            page: Número da página
            limit: Limite de resultados
            region: Região
            scenarios: Cenários (0 = todos)
            duration: Duração (0 = todas)
        """
        # URL encode para arrays vazios
        placements = "%5B%5D"  # []
        themes = "%5B%5D"
        genres = "%5B%5D"
        moods = "%5B%5D"

        endpoint = f"/api/trending/commercial-music-library?page={page}&limit={limit}&region={region}&scenarios={scenarios}&duration={duration}&placements={placements}&themes={themes}&genres={genres}&moods={moods}"
        return self._make_request(endpoint)

    def get_top_products(self, page: int = 1, last: int = 7,
                        order_by: str = "post", order_type: str = "desc") -> Dict[str, Any]:
        """
        Obter produtos em alta

        Args:
            page: Número da página
            last: Últimos N dias
            order_by: Ordenar por (post, sales, etc)
            order_type: Tipo de ordenação (desc, asc)
        """
        endpoint = f"/api/trending/top-products?page={page}&last={last}&order_by={order_by}&order_type={order_type}"
        return self._make_request(endpoint)

    def get_top_product_detail(self, product_id: str) -> Dict[str, Any]:
        """
        Obter detalhes de produto em alta

        Args:
            product_id: ID do produto
        """
        endpoint = f"/api/trending/top-products/detail?product_id={product_id}"
        return self._make_request(endpoint)

    def get_top_product_metrics(self, product_id: str) -> Dict[str, Any]:
        """
        Obter métricas de produto em alta

        Args:
            product_id: ID do produto
        """
        endpoint = f"/api/trending/top-products/metrics?product_id={product_id}"
        return self._make_request(endpoint)

    # ==========================================
    # CHALLENGE (HASHTAG) ENDPOINTS (2)
    # ==========================================

    def get_challenge_info(self, challenge_name: str) -> Dict[str, Any]:
        """
        Obter informações de uma hashtag/challenge

        Args:
            challenge_name: Nome da hashtag (sem #)
        """
        endpoint = f"/api/challenge/info?challengeName={challenge_name}"
        return self._make_request(endpoint)

    def get_challenge_posts(self, challenge_id: str, count: int = DEFAULT_COUNT,
                           cursor: int = DEFAULT_CURSOR) -> Dict[str, Any]:
        """
        Obter posts de uma hashtag/challenge

        Args:
            challenge_id: ID da challenge
            count: Quantidade de posts
            cursor: Cursor para paginação
        """
        endpoint = f"/api/challenge/posts?challengeId={challenge_id}&count={count}&cursor={cursor}"
        return self._make_request(endpoint)

    # ==========================================
    # PLACE ENDPOINTS (2)
    # ==========================================

    def get_place_info(self, place_id: str) -> Dict[str, Any]:
        """
        Obter informações de um local

        Args:
            place_id: ID do local
        """
        endpoint = f"/api/place/info?placeId={place_id}"
        return self._make_request(endpoint)

    def get_place_posts(self, place_id: str, count: int = DEFAULT_COUNT,
                       cursor: int = DEFAULT_CURSOR) -> Dict[str, Any]:
        """
        Obter posts de um local

        Args:
            place_id: ID do local
            count: Quantidade de posts
            cursor: Cursor para paginação
        """
        endpoint = f"/api/place/posts?placeId={place_id}&count={count}&cursor={cursor}"
        return self._make_request(endpoint)


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def print_json(data: Dict[str, Any]) -> None:
    """Pretty print JSON"""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    """Exemplo de uso"""
    api = TikTokAPI23()

    print("🎵 TikTok API23 - Teste de Conexão\n")

    # Teste: Buscar usuário
    print("📱 Buscando info do usuário @tiktok...")
    result = api.get_user_info("tiktok")
    print_json(result)


if __name__ == "__main__":
    main()
