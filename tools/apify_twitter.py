#!/usr/bin/env python3
"""
Apify Twitter Scraper - Ferramenta completa para scraping de tweets

Recursos:
- Busca avançada com filtros (data, mídia, verificados, etc)
- Scraping de perfis (tweets históricos)
- Scraping de tweets específicos (URLs)
- Scraping de replies/conversas
- Scraping de listas do Twitter
- Geolocalização
- Filtros de engajamento (min retweets, likes, replies)
- Query Wizard para construir buscas complexas

Pricing: $0.30 por 1000 tweets | 30-80 tweets/segundo
Actor ID: 61RPP7dywgiy0JPD0
"""

import sys
import os
import json
import time
from typing import List, Dict, Optional, Union
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apify_client import ApifyClient
from config.apify_config import APIFY_API_TOKEN, APIFY_TWITTER_ACTOR_ID


class ApifyTwitterScraper:
    """Cliente para o Apify Twitter Scraper"""

    def __init__(self, api_token: str = APIFY_API_TOKEN):
        """
        Inicializa o cliente Apify

        Args:
            api_token: Token da API do Apify
        """
        self.client = ApifyClient(api_token)
        self.actor_id = APIFY_TWITTER_ACTOR_ID

    def scrape(
        self,
        # URLs
        start_urls: Optional[List[str]] = None,

        # Buscas
        search_terms: Optional[List[str]] = None,
        twitter_handles: Optional[List[str]] = None,
        conversation_ids: Optional[List[str]] = None,

        # Limites
        max_items: Optional[int] = None,

        # Filtros básicos
        tweet_language: Optional[str] = None,
        only_verified_users: bool = False,
        only_twitter_blue: bool = False,
        only_image: bool = False,
        only_video: bool = False,
        only_quote: bool = False,

        # Filtros de usuário
        author: Optional[str] = None,
        in_reply_to: Optional[str] = None,
        mentioning: Optional[str] = None,

        # Filtros de localização
        geotagged_near: Optional[str] = None,
        within_radius: Optional[str] = None,
        geocode: Optional[str] = None,
        place_object_id: Optional[str] = None,

        # Filtros de engajamento
        minimum_retweets: Optional[int] = None,
        minimum_favorites: Optional[int] = None,
        minimum_replies: Optional[int] = None,

        # Filtros de data
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,

        # Ordenação
        sort: str = "Latest",  # Latest, Top, Relevance

        # Opções avançadas
        include_search_terms: bool = False,
        custom_map_function: Optional[str] = None,

        # Controle
        wait_for_finish: bool = True,
        timeout_secs: int = 300
    ) -> Dict:
        """
        Executa scraping de tweets

        Args:
            start_urls: Lista de URLs do Twitter (tweets, perfis, listas)
            search_terms: Termos de busca (suporta operadores avançados)
            twitter_handles: Lista de handles (@usuario)
            conversation_ids: IDs de conversas para buscar replies
            max_items: Número máximo de tweets para retornar
            tweet_language: Código ISO 639-1 do idioma (ex: 'pt', 'en')
            only_verified_users: Apenas usuários verificados
            only_twitter_blue: Apenas Twitter Blue
            only_image: Apenas tweets com imagens
            only_video: Apenas tweets com vídeos
            only_quote: Apenas quote tweets
            author: Handle do autor (sem @)
            in_reply_to: Handle do usuário sendo respondido (sem @)
            mentioning: Handle do usuário mencionado (sem @)
            geotagged_near: Local para busca geográfica
            within_radius: Raio da busca geográfica
            geocode: Lat/long para geocoding
            place_object_id: ID do lugar no Twitter
            minimum_retweets: Número mínimo de retweets
            minimum_favorites: Número mínimo de likes
            minimum_replies: Número mínimo de replies
            start_date: Data inicial (YYYY-MM-DD)
            end_date: Data final (YYYY-MM-DD)
            sort: Ordenação (Latest, Top, Relevance)
            include_search_terms: Incluir termo de busca nos resultados
            custom_map_function: Função customizada para processar resultados
            wait_for_finish: Aguardar conclusão do scraping
            timeout_secs: Timeout em segundos

        Returns:
            Dict com status e resultados
        """
        # Monta o input do actor
        run_input = {}

        # URLs
        if start_urls:
            run_input["startUrls"] = start_urls

        # Buscas
        if search_terms:
            run_input["searchTerms"] = search_terms
        if twitter_handles:
            run_input["twitterHandles"] = twitter_handles
        if conversation_ids:
            run_input["conversationIds"] = conversation_ids

        # Limites
        if max_items:
            run_input["maxItems"] = max_items

        # Filtros básicos
        if tweet_language:
            run_input["tweetLanguage"] = tweet_language
        if only_verified_users:
            run_input["onlyVerifiedUsers"] = True
        if only_twitter_blue:
            run_input["onlyTwitterBlue"] = True
        if only_image:
            run_input["onlyImage"] = True
        if only_video:
            run_input["onlyVideo"] = True
        if only_quote:
            run_input["onlyQuote"] = True

        # Filtros de usuário
        if author:
            run_input["author"] = author
        if in_reply_to:
            run_input["inReplyTo"] = in_reply_to
        if mentioning:
            run_input["mentioning"] = mentioning

        # Filtros de localização
        if geotagged_near:
            run_input["geotaggedNear"] = geotagged_near
        if within_radius:
            run_input["withinRadius"] = within_radius
        if geocode:
            run_input["geocode"] = geocode
        if place_object_id:
            run_input["placeObjectId"] = place_object_id

        # Filtros de engajamento
        if minimum_retweets:
            run_input["minimumRetweets"] = minimum_retweets
        if minimum_favorites:
            run_input["minimumFavorites"] = minimum_favorites
        if minimum_replies:
            run_input["minimumReplies"] = minimum_replies

        # Filtros de data
        if start_date:
            run_input["start"] = start_date
        if end_date:
            run_input["end"] = end_date

        # Ordenação
        run_input["sort"] = sort

        # Opções avançadas
        if include_search_terms:
            run_input["includeSearchTerms"] = True
        if custom_map_function:
            run_input["customMapFunction"] = custom_map_function

        print(f"🐦 Iniciando scraping do Twitter...")
        print(f"📊 Configuração:")
        if search_terms:
            print(f"   🔍 Termos: {', '.join(search_terms)}")
        if twitter_handles:
            print(f"   👤 Handles: {', '.join(twitter_handles)}")
        if start_urls:
            print(f"   🔗 URLs: {len(start_urls)} URL(s)")
        if max_items:
            print(f"   📈 Max items: {max_items}")

        # Inicia o actor
        run = self.client.actor(self.actor_id).call(run_input=run_input)

        if not wait_for_finish:
            return {
                "status": "running",
                "run_id": run["id"],
                "message": "Scraping iniciado. Use o run_id para verificar status."
            }

        # Aguarda conclusão
        print(f"⏳ Aguardando conclusão do scraping...")

        # Busca os resultados
        results = []
        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append(item)

        print(f"\n✅ Scraping concluído!")
        print(f"📊 Total de tweets coletados: {len(results)}")

        # Estatísticas
        stats = self._calculate_stats(results)

        return {
            "status": "success",
            "run_id": run["id"],
            "total_items": len(results),
            "stats": stats,
            "items": results
        }

    def _calculate_stats(self, results: List[Dict]) -> Dict:
        """Calcula estatísticas dos resultados"""
        if not results:
            return {}

        stats = {
            "total_tweets": len(results),
            "total_retweets": sum(item.get("retweetCount", 0) for item in results),
            "total_likes": sum(item.get("likeCount", 0) for item in results),
            "total_replies": sum(item.get("replyCount", 0) for item in results),
            "total_quotes": sum(item.get("quoteCount", 0) for item in results),
            "languages": {},
            "authors": {},
            "has_media": 0,
            "has_video": 0,
            "has_image": 0,
            "is_retweet": 0,
            "is_quote": 0,
            "is_reply": 0
        }

        for item in results:
            # Idiomas
            lang = item.get("lang", "unknown")
            stats["languages"][lang] = stats["languages"].get(lang, 0) + 1

            # Autores
            author = item.get("author", {}).get("userName", "unknown")
            stats["authors"][author] = stats["authors"].get(author, 0) + 1

            # Tipos
            if item.get("isRetweet"):
                stats["is_retweet"] += 1
            if item.get("isQuote"):
                stats["is_quote"] += 1
            if item.get("isReply"):
                stats["is_reply"] += 1

            # Mídia
            media = item.get("media", [])
            if media:
                stats["has_media"] += 1
                for m in media:
                    if m.get("type") == "video":
                        stats["has_video"] += 1
                    elif m.get("type") == "photo":
                        stats["has_image"] += 1

        return stats

    def scrape_profile_historical(
        self,
        handle: str,
        start_year: int,
        end_year: int,
        tweets_per_month: int = 800,
        max_items: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """
        Scraping histórico de perfil dividido por período

        Twitter retorna ~800 tweets por busca. Para coletar histórico completo,
        divide a busca em períodos mensais.

        Args:
            handle: Handle do Twitter (sem @)
            start_year: Ano inicial
            end_year: Ano final
            tweets_per_month: Tweets esperados por mês (ajustar se necessário)
            max_items: Limite total de tweets
            **kwargs: Outros parâmetros do scrape()

        Returns:
            Dict com resultados consolidados
        """
        print(f"🐦 Scraping histórico de @{handle}")
        print(f"📅 Período: {start_year} - {end_year}")

        # Gera queries divididas por mês
        search_terms = []
        current_year = start_year

        while current_year <= end_year:
            for month in range(1, 13):
                # Monta datas
                start_date = f"{current_year}-{month:02d}-01"

                # Próximo mês
                next_month = month + 1
                next_year = current_year
                if next_month > 12:
                    next_month = 1
                    next_year += 1

                end_date = f"{next_year}-{next_month:02d}-01"

                # Adiciona query
                query = f"from:{handle} since:{start_date} until:{end_date}"
                search_terms.append(query)

            current_year += 1

        print(f"📊 Total de queries: {len(search_terms)}")
        print(f"⚠️  Isso pode levar alguns minutos...")

        # Executa scraping
        result = self.scrape(
            search_terms=search_terms,
            max_items=max_items,
            **kwargs
        )

        return result

    def scrape_conversation(
        self,
        tweet_id: str,
        hashtag: Optional[str] = None,
        max_items: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """
        Scraping de uma conversa (replies de um tweet)

        Args:
            tweet_id: ID do tweet
            hashtag: Filtrar replies com hashtag específica (opcional)
            max_items: Limite de replies
            **kwargs: Outros parâmetros do scrape()

        Returns:
            Dict com replies
        """
        query = f"conversation_id:{tweet_id}"
        if hashtag:
            query += f" #{hashtag}"

        return self.scrape(
            search_terms=[query],
            max_items=max_items,
            **kwargs
        )


def main():
    """Função principal para testes"""
    import argparse

    parser = argparse.ArgumentParser(description="Apify Twitter Scraper")
    parser.add_argument("--search", nargs="+", help="Termos de busca")
    parser.add_argument("--handles", nargs="+", help="Twitter handles")
    parser.add_argument("--urls", nargs="+", help="URLs do Twitter")
    parser.add_argument("--max-items", type=int, help="Máximo de tweets")
    parser.add_argument("--lang", help="Idioma (pt, en, etc)")
    parser.add_argument("--verified", action="store_true", help="Apenas verificados")
    parser.add_argument("--blue", action="store_true", help="Apenas Twitter Blue")
    parser.add_argument("--image", action="store_true", help="Apenas com imagens")
    parser.add_argument("--video", action="store_true", help="Apenas com vídeos")
    parser.add_argument("--output", default="twitter_results.json", help="Arquivo de saída")

    args = parser.parse_args()

    # Valida input
    if not args.search and not args.handles and not args.urls:
        parser.error("Informe pelo menos --search, --handles ou --urls")

    # Executa scraping
    scraper = ApifyTwitterScraper()
    result = scraper.scrape(
        search_terms=args.search,
        twitter_handles=args.handles,
        start_urls=args.urls,
        max_items=args.max_items,
        tweet_language=args.lang,
        only_verified_users=args.verified,
        only_twitter_blue=args.blue,
        only_image=args.image,
        only_video=args.video
    )

    # Salva resultados
    output_path = os.path.expanduser(f"~/Downloads/{args.output}")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Resultados salvos em: {output_path}")
    print(f"📊 Estatísticas:")
    if result.get("stats"):
        stats = result["stats"]
        print(f"   Total de tweets: {stats.get('total_tweets', 0)}")
        print(f"   Total de retweets: {stats.get('total_retweets', 0)}")
        print(f"   Total de likes: {stats.get('total_likes', 0)}")
        print(f"   Total de replies: {stats.get('total_replies', 0)}")


if __name__ == "__main__":
    main()
