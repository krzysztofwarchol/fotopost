from app.models import User, Post


def recommend_users(user_id):

    user = User.objects.get(id=user_id)

    user_followings = user.following.all()

    posts = Post.objects.filter(creater=user)

    content_tags = [pt.tag.name_tag for p in posts for pt in p.post_tags.all()]

    content_tags = list(set(content_tags))

    other_users = (
        User.objects.exclude(id__in=[f.id for f in user_followings])
        .exclude(id=user_id)
        .exclude(is_superuser=True)
    )

    scores = {}

    for u in other_users:

        posts = Post.objects.filter(creater=u)

        score = 0

        for tag in content_tags:

            tagged_posts = posts.filter(post_tags__tag__name_tag=tag)

            tagged_post_count = len(tagged_posts)

            tagged_likes_per_post = (
                sum([p.likers.count() for p in tagged_posts]) / tagged_post_count
                if tagged_post_count > 0
                else 0
            )

            score += tagged_post_count * 0.5 + tagged_likes_per_post * 0.1

        scores[u] = score

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print(sorted_scores)

    recommendations = [u for u, s in sorted_scores[:10]]

    return recommendations
