# Engagement & Authenticity Strategy (Phase 7+)

To make Lena-Marie feel like a real person, we need to go beyond "Post & Forget". We need **Interaction**.

## 1. Comment Management (The "Community" Layer)
**Goal**: Reply to comments on her posts to boost the algorithm and build a connection.
*   **Technical Implementation**:
    *   `bot.get_latest_comments(media_id)`: Fetch comments.
    *   **Filter**: Ignore emojis-only or spam.
    *   **Ollama Intelligence**:
        *   System Prompt: "You are replying to a fan. Keep it short, friendly, use German if they write German."
        *   Input: "User wrote: 'Cool setup!'" -> Output: "Thanks! It's a cable mess though 🙈"
    *   **Action**: `bot.reply_comment(comment_id, text)`.
*   **Risk**: High interaction rate can trigger spam filters. Limit to 5-10 replies/hour.

## 2. Story Telling (The "Daily Life" Layer)
**Goal**: Show "Behind the Scenes" content that vanishes after 24h.
*   **Content Types**:
    *   **"POV" Shots**: A photo of a laptop screen, a coffee cup, a hiking trail (no face needed).
    *   **Reposts**: Sharing her new feed post to the story ("New post up! 🚀").
*   **Technical Implementation**:
    *   Use ComfyUI with a **9:16 Aspect Ratio** workflow.
    *   `bot.upload_story(path, caption)`.

## 3. Targeted Networking (The "Growth" Layer)
**Goal**: Engage with the specific niches: #DevOps, #Gorpcore, #Berlin.
*   **Strategy**:
    *   Search for hashtags.
    *   Like the "Top" posts (higher quality).
    *   *Occasionally* comment (very risky, maybe manual first).
*   **Technical Implementation**:
    *   `bot.get_hashtag_medias("devops")`.
    *   `bot.like_media(media_id)`.

## 4. Visual Variety (The "Human" Layer)
**Goal**: Don't just post the face every time. It looks uncanny.
*   **Idea**:
    *   Create a "Context Mix": 1 Face Post : 2 Context Posts.
    *   **Context Prompts**: "A cluttered desk with a mechanical keyboard and a mate drink, 35mm style", "A foggy view from a mountain peak, boots visible."

## 5. DM Handling (The "Safety" Layer)
**Goal**: Don't ignore DMs, but don't get scammed.
*   **Strategy**:
    *   **Status**: ✅ IMPLEMENTED (V7).
    *   **Features**:
        *   Auto-Accepts Pending Requests.
        *   **Context Aware**: Remembers last 5 messages.
        *   **Persona**: Native Gen-Z German, Emojis, "Single" status, Bavarian Holidays.
        *   **Language Detection**: Automagically switches DE/EN.
    *   **Technical Implementation**: `scripts/reply_dms.py`.

## Architecture Update Required
We need a **Scheduler Loop** (e.g., running every 30 mins) that:
1.  Checks for new comments? -> Reply.
2.  Is it 10:00 AM? -> Post Story.
3.  Is it 18:00 PM? -> Post Feed.
