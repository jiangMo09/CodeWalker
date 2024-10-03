import asyncio
from utils.redis_client import execute_redis_command, get_redis_client


async def update_leaderboard(
    question_id: int, execution_time: float, username: str, score: float
):
    redis = await get_redis_client()
    question_leaderboard_key = f"{{leaderboard}}:question:{question_id}"
    total_leaderboard_key = "{leaderboard}:total"

    max_retries = 3
    for attempt in range(max_retries):
        try:
            pipe = redis.pipeline()

            # get other question scores
            for i in range(1, 6):
                if i != question_id:
                    pipe.zscore(f"{{leaderboard}}:question:{i}", username)

            result = await execute_redis_command(pipe.execute)

            # new total scores
            answered_questions = sum(1 for score in result if score is not None)
            max_score_per_question = 20
            total_max_score = answered_questions * max_score_per_question

            other_scores_sum = sum(float(score) if score else 0 for score in result)

            new_total_score = round(total_max_score - other_scores_sum + score, 2)

            pipe = redis.pipeline()
            # update current score
            pipe.zadd(question_leaderboard_key, {username: execution_time})
            # update total scores
            pipe.zadd(total_leaderboard_key, {username: new_total_score})
            await execute_redis_command(pipe.execute)

            total = await execute_redis_command(redis.zcard, question_leaderboard_key)
            slower_count = await execute_redis_command(
                redis.zcount, question_leaderboard_key, execution_time, "+inf"
            )

            if total > 1:
                percentile = min(99, max(1, (slower_count * 100) // (total - 1)))
            else:
                percentile = 99

            return percentile

        except (ValueError, Exception) as e:
            if attempt == max_retries - 1:
                print(f"Error updating leaderboard: {str(e)}")
                raise
            await asyncio.sleep(0.1 * (attempt + 1))

    raise Exception("Failed to update leaderboard after multiple attempts")

async def get_total_leaderboard(limit: int = 10):
    redis = await get_redis_client()
    leaderboard_key = "{leaderboard}:total"

    try:
        leaderboard_data = await execute_redis_command(
            redis.zrange, leaderboard_key, 0, limit - 1, withscores=True, desc=True
        )

        leaderboard = [
            {
                "username": username,
                "score": round(float(score), 2),
            }
            for username, score in leaderboard_data
        ]

        return leaderboard
    except Exception as e:
        print(f"Error getting total leaderboard: {str(e)}")
        raise
