#!/usr/bin/env python3
"""
Script para obter insights e métricas do Instagram via Instagram Graph API

Funcionalidades:
- ✅ Métricas da conta (seguidores, alcance, impressões)
- ✅ Métricas de posts específicos (curtidas, comentários, salvamentos)
- ✅ Métricas de Reels (visualizações, curtidas, compartilhamentos)
- ✅ Lista de posts recentes com métricas
- ✅ Exportação para JSON

Uso:
    # Métricas da conta
    python3 get_instagram_insights.py account

    # Métricas de um post/reel específico
    python3 get_instagram_insights.py media MEDIA_ID

    # Listar posts recentes com métricas
    python3 get_instagram_insights.py recent --limit 10

    # Exportar para JSON
    python3 get_instagram_insights.py account --output insights.json
"""

import requests
import sys
import os
import argparse
import json
from datetime import datetime

# Importar configurações
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import instagram_config as config


class InstagramInsights:
    """Classe para obter insights do Instagram"""

    def __init__(self):
        self.user_id = config.INSTAGRAM_USER_ID
        self.access_token = config.INSTAGRAM_ACCESS_TOKEN
        self.endpoints = config.ENDPOINTS

    def get_account_insights(self):
        """Obtém insights da conta"""
        print("📊 INSIGHTS DA CONTA")
        print("=" * 60)
        print(f"📱 Conta: @{config.INSTAGRAM_USERNAME}")
        print(f"🆔 User ID: {self.user_id}")
        print("=" * 60)

        insights = {}

        try:
            # Obter informações básicas da conta
            response = requests.get(
                f"{self.endpoints['get_media']}/{self.user_id}",
                params={
                    "fields": "followers_count,follows_count,media_count,username,name,biography,website,profile_picture_url",
                    "access_token": self.access_token
                }
            )
            response.raise_for_status()
            account_data = response.json()

            followers_count = account_data.get("followers_count", 0)
            follows_count = account_data.get("follows_count", 0)
            media_count = account_data.get("media_count", 0)
            username = account_data.get("username", "N/A")
            name = account_data.get("name", "N/A")
            bio = account_data.get("biography", "")
            website = account_data.get("website", "")

            print(f"\n👤 PERFIL")
            print(f"   Nome: {name}")
            print(f"   Username: @{username}")
            if bio:
                print(f"   Bio: {bio[:100]}{'...' if len(bio) > 100 else ''}")
            if website:
                print(f"   Site: {website}")

            print(f"\n📈 ESTATÍSTICAS")
            print(f"   👥 Seguidores: {followers_count:,}")
            print(f"   ➡️  Seguindo: {follows_count:,}")
            print(f"   📸 Posts: {media_count:,}")

            insights["profile"] = {
                "username": username,
                "name": name,
                "biography": bio,
                "website": website,
                "followers_count": followers_count,
                "follows_count": follows_count,
                "media_count": media_count
            }

            # Tentar obter insights avançados (requer permissões específicas)
            try:
                # Métricas dos últimos 30 dias
                metrics = "impressions,reach,profile_views"

                response_insights = requests.get(
                    f"{self.endpoints['get_media']}/{self.user_id}/insights",
                    params={
                        "metric": metrics,
                        "period": "days_28",
                        "access_token": self.access_token
                    }
                )

                if response_insights.status_code == 200:
                    insights_data = response_insights.json()
                    metrics_data = insights_data.get("data", [])

                    print(f"\n📊 MÉTRICAS (Últimos 28 dias)")

                    for metric in metrics_data:
                        metric_name = metric.get("name")
                        values = metric.get("values", [])
                        total = sum([v.get("value", 0) for v in values])

                        if metric_name == "impressions":
                            print(f"   👁️  Impressões: {total:,}")
                            insights["impressions_28d"] = total
                        elif metric_name == "reach":
                            print(f"   📢 Alcance: {total:,}")
                            insights["reach_28d"] = total
                        elif metric_name == "profile_views":
                            print(f"   👤 Visualizações do perfil: {total:,}")
                            insights["profile_views_28d"] = total

            except Exception as e:
                print(f"\n⚠️  Insights avançados não disponíveis: {e}")
                print("   (Requer permissões instagram_manage_insights)")

            return insights

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro ao obter insights da conta: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None

    def get_media_insights(self, media_id):
        """Obtém insights de um post/reel específico"""
        print(f"📊 INSIGHTS DO POST/REEL")
        print("=" * 60)
        print(f"🆔 Media ID: {media_id}")
        print("=" * 60)

        insights = {"media_id": media_id}

        try:
            # Obter informações básicas do post
            response = requests.get(
                f"{self.endpoints['get_media']}/{media_id}",
                params={
                    "fields": "id,media_type,media_url,thumbnail_url,permalink,caption,timestamp,like_count,comments_count,media_product_type",
                    "access_token": self.access_token
                }
            )
            response.raise_for_status()
            media_data = response.json()

            media_type = media_data.get("media_type", "UNKNOWN")
            media_product = media_data.get("media_product_type", "FEED")
            caption = media_data.get("caption", "")
            timestamp = media_data.get("timestamp", "")
            like_count = media_data.get("like_count", 0)
            comments_count = media_data.get("comments_count", 0)
            permalink = media_data.get("permalink", "")

            # Formatar timestamp
            if timestamp:
                try:
                    # Tentar formato padrão primeiro
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    timestamp_str = dt.strftime("%d/%m/%Y %H:%M")
                except:
                    # Formato alternativo do Instagram: 2025-10-31T21:52:50+0000
                    from datetime import datetime as dt_module
                    dt = dt_module.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
                    timestamp_str = dt.strftime("%d/%m/%Y %H:%M")
            else:
                timestamp_str = "N/A"

            print(f"\n📝 INFORMAÇÕES")
            print(f"   Tipo: {media_type} ({media_product})")
            print(f"   Data: {timestamp_str}")
            if caption:
                print(f"   Legenda: {caption[:80]}{'...' if len(caption) > 80 else ''}")
            if permalink:
                print(f"   Link: {permalink}")

            print(f"\n📈 MÉTRICAS BÁSICAS")
            print(f"   ❤️  Curtidas: {like_count:,}")
            print(f"   💬 Comentários: {comments_count:,}")

            insights.update({
                "media_type": media_type,
                "media_product_type": media_product,
                "caption": caption,
                "timestamp": timestamp,
                "like_count": like_count,
                "comments_count": comments_count,
                "permalink": permalink
            })

            # Tentar obter insights avançados
            try:
                # Métricas disponíveis dependem do tipo de mídia
                if media_product == "REELS":
                    metrics = "plays,reach,total_interactions,likes,comments,shares,saves"
                else:
                    metrics = "impressions,reach,engagement,saved"

                response_insights = requests.get(
                    f"{self.endpoints['get_media']}/{media_id}/insights",
                    params={
                        "metric": metrics,
                        "access_token": self.access_token
                    }
                )

                if response_insights.status_code == 200:
                    insights_data = response_insights.json()
                    metrics_data = insights_data.get("data", [])

                    print(f"\n📊 MÉTRICAS AVANÇADAS")

                    for metric in metrics_data:
                        metric_name = metric.get("name")
                        values = metric.get("values", [])
                        value = values[0].get("value", 0) if values else 0

                        label = {
                            "impressions": "👁️  Impressões",
                            "reach": "📢 Alcance",
                            "engagement": "💡 Engajamento",
                            "saved": "💾 Salvamentos",
                            "plays": "▶️  Reproduções",
                            "total_interactions": "👆 Interações totais",
                            "likes": "❤️  Curtidas (insights)",
                            "comments": "💬 Comentários (insights)",
                            "shares": "📤 Compartilhamentos",
                            "saves": "💾 Salvamentos"
                        }.get(metric_name, metric_name)

                        print(f"   {label}: {value:,}")
                        insights[metric_name] = value

                    # Calcular taxa de engajamento
                    if "reach" in insights and insights["reach"] > 0:
                        engagement_rate = (insights.get("engagement", 0) / insights["reach"]) * 100
                        print(f"\n   📈 Taxa de Engajamento: {engagement_rate:.2f}%")
                        insights["engagement_rate"] = engagement_rate

            except Exception as e:
                print(f"\n⚠️  Insights avançados não disponíveis: {e}")

            return insights

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro ao obter insights do post: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None

    def get_recent_media(self, limit=10):
        """Lista posts recentes com métricas básicas"""
        print("📊 POSTS RECENTES")
        print("=" * 60)
        print(f"📱 Conta: @{config.INSTAGRAM_USERNAME}")
        print(f"📋 Últimos {limit} posts")
        print("=" * 60)

        try:
            response = requests.get(
                f"{self.endpoints['get_media']}/{self.user_id}/media",
                params={
                    "fields": "id,media_type,media_product_type,caption,timestamp,like_count,comments_count,permalink",
                    "limit": limit,
                    "access_token": self.access_token
                }
            )
            response.raise_for_status()

            data = response.json()
            media_list = data.get("data", [])

            if not media_list:
                print("\n📭 Nenhum post encontrado")
                return []

            print(f"\n✅ Encontrados {len(media_list)} posts:\n")

            results = []

            for i, media in enumerate(media_list, 1):
                media_id = media.get("id")
                media_type = media.get("media_type", "UNKNOWN")
                media_product = media.get("media_product_type", "FEED")
                caption = media.get("caption", "")
                timestamp = media.get("timestamp", "")
                like_count = media.get("like_count", 0)
                comments_count = media.get("comments_count", 0)
                permalink = media.get("permalink", "")

                # Formatar timestamp
                if timestamp:
                    try:
                        # Tentar formato padrão primeiro
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timestamp_str = dt.strftime("%d/%m/%Y %H:%M")
                    except:
                        # Formato alternativo do Instagram: 2025-10-31T21:52:50+0000
                        from datetime import datetime as dt_module
                        dt = dt_module.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
                        timestamp_str = dt.strftime("%d/%m/%Y %H:%M")
                else:
                    timestamp_str = "N/A"

                # Calcular engajamento
                engagement = like_count + comments_count

                print(f"[{i}] {media_type} - {media_product}")
                print(f"    🆔 ID: {media_id}")
                print(f"    📅 {timestamp_str}")
                if caption:
                    print(f"    💬 {caption[:60]}{'...' if len(caption) > 60 else ''}")
                print(f"    ❤️  {like_count:,} curtidas | 💬 {comments_count:,} comentários | 💡 {engagement:,} engajamentos")
                if permalink:
                    print(f"    🔗 {permalink}")
                print()

                results.append({
                    "media_id": media_id,
                    "media_type": media_type,
                    "media_product_type": media_product,
                    "caption": caption,
                    "timestamp": timestamp,
                    "like_count": like_count,
                    "comments_count": comments_count,
                    "engagement": engagement,
                    "permalink": permalink
                })

            return results

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro ao listar posts: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return []
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []


def main():
    parser = argparse.ArgumentParser(
        description="Obter insights e métricas do Instagram via API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Insights da conta
  python3 get_instagram_insights.py account

  # Insights de um post/reel específico
  python3 get_instagram_insights.py media 18083282260953214

  # Listar 20 posts recentes
  python3 get_instagram_insights.py recent --limit 20

  # Exportar insights da conta para JSON
  python3 get_instagram_insights.py account --output account_insights.json

  # Exportar métricas de um post para JSON
  python3 get_instagram_insights.py media 18083282260953214 --output post_insights.json

Notas:
  - Insights avançados requerem permissão instagram_manage_insights
  - Métricas são atualizadas periodicamente pelo Instagram
  - Posts muito recentes podem não ter todas as métricas disponíveis
  - Reels têm métricas diferentes de posts normais
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Tipo de insights")

    # Subcomando: account
    parser_account = subparsers.add_parser("account", help="Insights da conta")
    parser_account.add_argument("--output", help="Arquivo JSON para exportar (opcional)")

    # Subcomando: media
    parser_media = subparsers.add_parser("media", help="Insights de um post/reel")
    parser_media.add_argument("media_id", help="ID do post/reel")
    parser_media.add_argument("--output", help="Arquivo JSON para exportar (opcional)")

    # Subcomando: recent
    parser_recent = subparsers.add_parser("recent", help="Lista posts recentes com métricas")
    parser_recent.add_argument("--limit", type=int, default=10, help="Número de posts (padrão: 10)")
    parser_recent.add_argument("--output", help="Arquivo JSON para exportar (opcional)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Criar instância
    insights_manager = InstagramInsights()

    # Executar comando
    result = None

    if args.command == "account":
        result = insights_manager.get_account_insights()

    elif args.command == "media":
        result = insights_manager.get_media_insights(args.media_id)

    elif args.command == "recent":
        result = insights_manager.get_recent_media(args.limit)

    # Exportar para JSON se solicitado
    if result and hasattr(args, 'output') and args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Dados exportados para: {args.output}")
        except Exception as e:
            print(f"\n❌ Erro ao exportar JSON: {e}")

    success = result is not None
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
