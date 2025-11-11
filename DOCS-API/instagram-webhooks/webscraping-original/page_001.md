# Webhooks Reference: Instagram

**URL:** https://developers.facebook.com/docs/graph-api/webhooks/reference/instagram

---

# Webhooks Reference: Instagram

Category of updates relating to activity on Instagram user

FBInstagramCommentsField

| Field | Description |
| --- | --- |
| `field`<br><br>string | Name of the updated field |
| `value`<br><br>object | value |
| `from`<br><br>IGCommentFromUser | Instagram-scoped ID and username of the Instagram user who created the comment |
| `id`<br><br>numeric string | id  |
| `username`<br><br>string | username |
| `self_ig_scoped_id`<br><br>numeric string | self ig scoped id |
| `media`<br><br>IGCommentMedia | ID and product type of the IG Media the comment was created on |
| `id`<br><br>numeric string | ID of the IG Media the comment was created on |
| `media_product_type`<br><br>string | Product type of the IG Media the comment was created on |
| `ad_id`<br><br>numeric string | ID of the IG Ad the comment was created on |
| `ad_title`<br><br>string | Title of the IG Ad the comment was created on |
| `original_media_id`<br><br>numeric string | original\_media\_id |
| `id`<br><br>numeric string | The id of the object |
| `parent_id`<br><br>numeric string | ID of parent IG Comment if this comment was created on another IG Comment (i.g. a reply to another comment) |
| `text`<br><br>string | Comment text |

## `messaging_handover`

FBInstagramHOPField

| Field | Description |
| --- | --- |
| `field`<br><br>string | Name of the updated field |
| `value`<br><br>object | value |
| `sender`<br><br>IDName | sender |
| `id`<br><br>id | ID  |
| `recipient`<br><br>IDName | recipient |
| `id`<br><br>id | ID  |
| `timestamp`<br><br>unsigned integer | timestamp |
| `pass_thread_control`<br><br>object | pass\_thread\_control |
| `previous_owner_app_id`<br><br>numeric string | previous\_owner\_app\_id |
| `new_owner_app_id`<br><br>numeric string | new\_owner\_app\_id |
| `metadata`<br><br>string | metadata |
| `take_thread_control`<br><br>object | take\_thread\_control |
| `previous_owner_app_id`<br><br>numeric string | previous\_owner\_app\_id |
| `new_owner_app_id`<br><br>numeric string | new\_owner\_app\_id |
| `metadata`<br><br>string | metadata |
| `request_thread_control`<br><br>object | request\_thread\_control |
| `requested_owner_app_id`<br><br>numeric string | requested\_owner\_app\_id |
| `metadata`<br><br>string | metadata |
| `app_roles`<br><br>map | app\_roles |

FBInstagramLiveCommentsField

| Field | Description |
| --- | --- |
| `field`<br><br>string | Name of the updated field |
| `value`<br><br>object | value |
| `from`<br><br>IGCommentFromUser | Instagram-scoped ID and username of the Instagram user who created the comment |
| `id`<br><br>numeric string | id  |
| `username`<br><br>string | username |
| `self_ig_scoped_id`<br><br>numeric string | self ig scoped id |
| `media`<br><br>IGCommentMedia | ID and product type of the IG Media the comment was created on |
| `id`<br><br>numeric string | ID of the IG Media the comment was created on |
| `media_product_type`<br><br>string | Product type of the IG Media the comment was created on |
| `ad_id`<br><br>numeric string | ID of the IG Ad the comment was created on |
| `ad_title`<br><br>string | Title of the IG Ad the comment was created on |
| `original_media_id`<br><br>numeric string | original\_media\_id |
| `id`<br><br>numeric string | The id of the object |
| `parent_id`<br><br>numeric string | ID of parent IG Comment if this comment was created on another IG Comment (i.g. a reply to another comment) |
| `text`<br><br>string | Comment text |

## `message_edit`

FBInstagramMessageEditField

| Field | Description |
| --- | --- |
| `field`<br><br>string | Name of the updated field |

## `message_reactions`

FBInstagramMessageReactionsField

| Field | Description |
| --- | --- |
| `field`<br><br>string | Name of the updated field |
| `value`<br><br>object | value |
| `sender`<br><br>IDName | sender |
| `id`<br><br>id | ID  |
| `recipient`<br><br>IDName | recipient |
| `id`<br><br>id | ID  |
| `timestamp`<br><br>unsigned integer | timestamp |
| `reaction`<br><br>object | reaction |
| `mid`<br><br>string | mid |
| `action`<br><br>enum | action |
| `reaction`<br><br>enum | reaction |
| `emoji`<br><br>string | emoji |
| `folder`<br><br>string | folder |

## `messages`

FBInstagramMessagesField

| Field | Description |
| --- | --- |
| `field`<br><br>string | Name of the updated field |
| `value`<br><br>object | value |
| `sender`<br><br>IDName | sender |
| `id`<br><br>id | ID  |
| `recipient`<br><br>IDName | recipient |
| `id`<br><br>id | ID  |
| `timestamp`<br><br>unsigned integer | timestamp |
| `message`<br><br>object | message |
| `attachments`<br><br>list<FBInstagramMessageAttachmentData> | attachments |
| `type`<br><br>string | type |
| `payload`<br><br>object | payload |
| `ig_post_media_id`<br><br>numeric string | ig post media id |
| `url`<br><br>string | for url field in message attachment |
| `generic`<br><br>map | for generic template data field in message attachment |
| `reply_to`<br><br>object | reply\_to |
| `story`<br><br>object | story |
| `url`<br><br>string | url |
| `id`<br><br>string | id  |
| `link_sticker_url`<br><br>string | link sticker url |
| `is_self`<br><br>bool | is self |
| `is_deleted`<br><br>bool | is\_deleted |
| `folder`<br><br>string | folder |

## `mentions`

Notifies you when an Instagram User @mentions you in a comment or caption on a media object.

| Field | Description |
| --- | --- |
| `field`<br><br>string | Name of the updated field |
| `value`<br><br>object | Contents of the update |
| `media_id`<br><br>string | ID of media containing comment with mention. |
| `comment_id`<br><br>string | ID of comment with mention. |

## `messaging_referral`

InstagramMessagingReferralField

| Field | Description |
| --- | --- |
| `field`<br><br>string | Name of the updated field |
| `value`<br><br>object | the referral information along with sender and business ids, and timestamp |
| `sender`<br><br>MessengerParticipantID | sender |
| `id`<br><br>numeric string | id  |
| `recipient`<br><br>MessengerParticipantID | recipient |
| `id`<br><br>numeric string | id  |
| `timestamp`<br><br>unsigned integer | timestamp |
| `referral`<br><br>object | referral |

## `messaging_seen`

InstagramMessagingSeenField

| Field | Description |
| --- | --- |
| `field`<br><br>string | Name of the updated field |
| `value`<br><br>object | Contents of the seen state update |
| `sender`<br><br>IDName | sender |
| `id`<br><br>id | ID  |
| `recipient`<br><br>IDName | recipient |
| `id`<br><br>id | ID  |
| `timestamp`<br><br>unsigned integer | timestamp |
| `read`<br><br>object | read |

## `messaging_postbacks`

InstagramPostbackField

| Field | Description |
| --- | --- |
| `field`<br><br>string | Name of the updated field |
| `value`<br><br>object | value |
| `sender`<br><br>IDName | sender of the postback |
| `id`<br><br>id | ID  |
| `recipient`<br><br>IDName | recipient |
| `id`<br><br>id | ID  |
| `is_self`<br><br>bool | is self |
| `timestamp`<br><br>unsigned integer | timestamp when it was sent |
| `postback`<br><br>object | postback payload |
| `title`<br><br>string | title of postback |
| `payload`<br><br>string | payload of postback |
| `referral`<br><br>object | referral details |
| `mid`[](https://developers.facebook.com/docs/graph-api/webhooks/reference/instagram#)<br><br>string | mid |

## `standby`

InstagramStandbyField

| Field | Description |
| --- | --- |
| `field`<br><br>string | Name of the updated field |
| `value`<br><br>string | value |

## `story_insights`

Notifies you when a story expires. Metrics with counts of less than 5 will be returned as `-1`.

| Field | Description |
| --- | --- |
| `field`<br><br>string | Name of the updated field |
| `value`<br><br>object | The result values |
| `media_id`<br><br>numeric string | Media Id of the Story |
| `impressions`<br><br>integer | Impressions |
| `reach`<br><br>integer | Reach |
| `taps_forward`<br><br>integer | Taps forward |
| `taps_back`<br><br>integer | Taps back |
| `exits`<br><br>integer | Exits |
| `replies`<br><br>integer | Replies |