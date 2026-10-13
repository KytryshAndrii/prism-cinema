from utils.connection import get_connection

def get_subscription_plans_logic():
    """
    Returns all subscription plans.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                subscription_plan_id,
                subscription_plan_type,
                subscription_plan_cost,
                subscription_plan_description
            FROM "SERVICE_SUBSCRIPTION_PLANS"
        """)
        rows = cur.fetchall()

        plans = []
        for row in rows:
            plans.append({
                "id": str(row[0]),
                "sub_type": row[1],
                "sub_cost": str(row[2]),
                "sub_description": row[3],
            })
        return plans
    finally:
        cur.close()
        conn.close()


def subscribe_to_plan_logic(user_id, plan_id):
    """
    Subscribes a user to a plan.
    Returns status code + optional error message.
    """
    if not user_id or not plan_id:
        return {"error": "Missing data"}, 400

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT subscription_plan_type
            FROM "SERVICE_SUBSCRIPTION_PLANS"
            WHERE subscription_plan_id = %s
        """, (plan_id,))
        plan = cur.fetchone()

        if not plan:
            return {"error": "Subscription plan not found"}, 404

        plan_type = plan[0]

        is_subscribed = plan_type.lower() != "free"

        cur.execute("""
            UPDATE "USERS"
            SET user_is_subscribed = %s,
                user_subscription_plan_id = %s
            WHERE user_id = %s
        """, (is_subscribed, plan_id, user_id))

        conn.commit()
        return None, 200

    except Exception as e:
        print("Subscription error:", e)
        return {"error": "Internal server error"}, 500

    finally:
        cur.close()
        conn.close()


def check_user_free_logic(user_id):
    """
    Returns True if the user is on a free plan, False if paid.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT user_is_subscribed
            FROM "USERS"
            WHERE user_id = %s
        """, (str(user_id),))
        result = cur.fetchone()

        if result is None:
            return {"error": "User not found"}, 404

        return not result[0], 200
    finally:
        cur.close()
        conn.close()


def get_user_subscription_plan_logic(user_id):
    """
    Returns the subscription plan info for a given user.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT s.subscription_plan_type, s.subscription_plan_id
            FROM "USERS" u
            LEFT JOIN "SERVICE_SUBSCRIPTION_PLANS" s
            ON u.user_subscription_plan_id = s.subscription_plan_id
            WHERE u.user_id = %s
        """, (str(user_id),))

        result = cur.fetchone()

        if not result or result[0] is None:
            return None, 200

        return {
            "id": str(result[1]),
            "sub_type": result[0]
        }, 200
    finally:
        cur.close()
        conn.close()
