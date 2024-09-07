from utils.redis_client import async_redis_client


async def update_leaderboard(
    question_id: int, execution_time: float, username: str, score: float
):

    async with async_redis_client as redis:
        question_leaderboard_key = f"{{leaderboard}}:question:{question_id}"
        total_leaderboard_key = "{leaderboard}:total"

        try:
            pipe = redis.pipeline()

            pipe.zscore(question_leaderboard_key, username)
            pipe.zscore(total_leaderboard_key, username)
            old_execution_time, current_total_score = await pipe.execute()

            old_execution_time = (
                float(old_execution_time) if old_execution_time else float("inf")
            )
            current_total_score = (
                float(current_total_score) if current_total_score else 0
            )

            old_score = max(0, 20 - old_execution_time)

            new_total_score = round(current_total_score - old_score + score, 2)

            pipe = redis.pipeline()
            pipe.zadd(question_leaderboard_key, {username: execution_time})
            pipe.zadd(total_leaderboard_key, {username: new_total_score})
            await pipe.execute()

            total = await redis.zcard(question_leaderboard_key)
            slower_count = await redis.zcount(
                question_leaderboard_key, execution_time, "+inf"
            )

            if total > 1:
                percentile = min(99, max(1, (slower_count * 100) // (total - 1)))
            else:
                percentile = 99

            return percentile

        except Exception as e:
            print(f"Error updating leaderboard: {str(e)}")
            raise


async def get_total_leaderboard(limit: int = 10):
    leaderboard_key = "{leaderboard}:total"

    leaderboard_data = await async_redis_client.zrange(
        leaderboard_key, 0, limit - 1, withscores=True, desc=True
    )

    leaderboard = [
        {
            "username": (
                username.decode("utf-8") if isinstance(username, bytes) else username
            ),
            "score": round(float(score), 2),
        }
        for username, score in leaderboard_data
    ]

    return leaderboard