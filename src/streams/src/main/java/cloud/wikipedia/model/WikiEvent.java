package cloud.wikipedia.model;

import com.google.gson.annotations.SerializedName;

public class WikiEvent {
  public WikiEvent(
      Long eventId,
      String title,
      String userType,
      String username,
      String dateTime,
      String language,
      String type,
      Boolean isRevert) {
    this.eventId = eventId;
    this.title = title;
    this.userType = userType;
    this.username = username;
    this.dateTime = dateTime;
    this.language = language;
    this.type = type;
    this.isRevert = isRevert;
  }

  @SerializedName("event_id")
  private Long eventId;

  @SerializedName("title")
  private String title;

  @SerializedName("user_type")
  private String userType;

  @SerializedName("username")
  private String username;

  @SerializedName("timestamp")
  private String dateTime;

  @SerializedName("language")
  private String language;

  @SerializedName("event_type")
  private String type;

  @SerializedName("is_revert")
  private Boolean isRevert;

  public Long getEventId() {
    return eventId;
  }

  public String getTitle() {
    return title;
  }

  public String getUserType() {
    return userType;
  }

  public String getUsername() {
    return username;
  }

  public String getDateTime() {
    return dateTime;
  }

  public String getLanguage() {
    return language;
  }

  public String getType() {
    return type;
  }

  public Boolean isRevert() {
    return isRevert;
  }

  @Override
  public String toString() {
    return "WikiEvent{"
        + "eventId="
        + eventId
        + ", title='"
        + title
        + '\''
        + ", userType='"
        + userType
        + '\''
        + ", username='"
        + username
        + '\''
        + ", dateTime='"
        + dateTime
        + '\''
        + ", language='"
        + language
        + '\''
        + ", type='"
        + type
        + '\''
        + ", isRevert="
        + isRevert
        + '}';
  }
}
