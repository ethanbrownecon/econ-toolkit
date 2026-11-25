# Fun project: Your Spotify listening

Spotify Wrapped only shows what Spotify chooses to show. In this project you download your own listening history and analyze it yourself: your real top artists, when you listen, how your taste changes over time, and which artists you skip the most.

!!! info "What you will practice"
    Requesting your own data · reading JSON · converting time zones · grouping and summarizing · bar and line charts · thinking like an economist about revealed preference

    **Time:** about an hour. **Languages:** R or Python. Pick one in any tab and the whole page follows.

## Step 0: Request your data

Spotify takes a few days to prepare your data, so request it now and use the sample file while you wait.

1. Log in at [spotify.com/account/privacy](https://www.spotify.com/account/privacy/).
2. Scroll to **Download your data**.
3. Tick **Account data** and click **Request data**.
4. Confirm the request from the email Spotify sends you.
5. Within about five days, you get an email with a download link. Download and unzip the folder.

Your listening history is in files named `StreamingHistory_music_0.json`, `StreamingHistory_music_1.json` and so on. Older exports call them `StreamingHistory0.json`.

!!! tip "Practice with the sample file"
    The sample has six months of made-up listening (all artists are invented) in exactly Spotify's format. Every step below runs on it straight from this website.

    [:material-download: Download sample file](data/StreamingHistory_music_0.json){ .md-button download }

## Step 1: Load the data

Each play is one record with four fields:

| Field | Meaning |
|---|---|
| `endTime` | When the song stopped playing, in UTC |
| `artistName` | Artist |
| `trackName` | Song |
| `msPlayed` | How long it played, in milliseconds |

=== "R"

    ```r
    library(tidyverse)
    library(jsonlite)   # reads JSON files

    url <- "https://ethanbrownecon.github.io/econ-toolkit/projects/data/StreamingHistory_music_0.json"
    df <- as_tibble(fromJSON(url))
    head(df)
    ```

=== "Python"

    ```python
    import matplotlib.pyplot as plt
    import pandas as pd

    url = "https://ethanbrownecon.github.io/econ-toolkit/projects/data/StreamingHistory_music_0.json"
    df = pd.read_json(url)
    df.head()
    ```

??? note "Use your own data, including several files"
    Point the code at the unzipped folder. This reads every history file and stacks them:

    === "R"

        ```r
        files <- list.files("Spotify Account Data",
                            pattern = "^StreamingHistory_music_.*\\.json$",
                            full.names = TRUE)
        df <- as_tibble(bind_rows(lapply(files, fromJSON)))
        ```

    === "Python"

        ```python
        from pathlib import Path

        files = sorted(Path("Spotify Account Data").glob("StreamingHistory_music_*.json"))
        df = pd.concat([pd.read_json(f) for f in files], ignore_index=True)
        ```

## Step 2: Clean it

Three fixes:

1. **Time zone.** Spotify records times in UTC. Convert to your own time zone, or a song you played at 9 pm in New York shows up at 1 am. Change `America/New_York` to [your zone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones), such as `America/Chicago`, `America/Los_Angeles` or `Europe/London`.
2. **Minutes.** Milliseconds are hard to read. Divide by 60,000.
3. **Skips.** Spotify counts a play as a stream only after 30 seconds. Mark anything shorter as a skip.

=== "R"

    ```r
    df <- df %>% mutate(
      endTime = with_tz(ymd_hm(endTime, tz = "UTC"), "America/New_York"),
      minutes = msPlayed / 60000,
      skipped = msPlayed < 30000
    )

    plays <- filter(df, !skipped)
    ```

=== "Python"

    ```python
    df["endTime"] = (
        pd.to_datetime(df["endTime"])
        .dt.tz_localize("UTC")
        .dt.tz_convert("America/New_York")
    )
    df["minutes"] = df["msPlayed"] / 60_000
    df["skipped"] = df["msPlayed"] < 30_000

    plays = df[~df["skipped"]].copy()
    ```

**Check (sample file):** 5,273 records, of which 4,474 are real plays. That is about **254 hours** of music.

## Step 3: Your real top artists

Wrapped ranks by number of plays. Ranking by hours listened can tell a different story.

=== "R"

    ```r
    top_artists <- plays %>%
      summarise(hours = sum(minutes) / 60, .by = artistName) %>%
      arrange(desc(hours)) %>%
      head(10)

    ggplot(top_artists, aes(hours, fct_reorder(artistName, hours))) +
      geom_col(fill = "#0f766e") +
      labs(x = "Hours listened", y = NULL, title = "My top 10 artists")
    ```

=== "Python"

    ```python
    top_artists = (
        plays.groupby("artistName")["minutes"].sum()
        .div(60)
        .sort_values()
        .tail(10)
    )

    top_artists.plot.barh(color="#0f766e", title="My top 10 artists")
    plt.xlabel("Hours listened")
    plt.show()
    ```

**Check:** the sample listener's number one is *The Marginal Costs*, with about 86 hours.

And your most played songs:

=== "R"

    ```r
    plays %>% count(artistName, trackName, sort = TRUE) %>% head(10)
    ```

=== "Python"

    ```python
    plays.groupby(["artistName", "trackName"]).size().sort_values(ascending=False).head(10)
    ```

## Step 4: When do you listen?

### By hour of the day

=== "R"

    ```r
    plays %>%
      mutate(hour = hour(endTime)) %>%
      summarise(hours = sum(minutes) / 60, .by = hour) %>%
      ggplot(aes(hour, hours)) +
      geom_col(fill = "#0f766e") +
      labs(x = "Hour of the day", y = "Hours listened")
    ```

=== "Python"

    ```python
    by_hour = plays.groupby(plays["endTime"].dt.hour)["minutes"].sum() / 60
    by_hour.plot.bar(color="#0f766e")
    plt.xlabel("Hour of the day")
    plt.ylabel("Hours listened")
    plt.show()
    ```

### By day of the week

=== "R"

    ```r
    plays %>%
      mutate(day = wday(endTime, label = TRUE, week_start = 1)) %>%
      summarise(hours = sum(minutes) / 60, .by = day) %>%
      arrange(day)
    ```

=== "Python"

    ```python
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plays.groupby(plays["endTime"].dt.day_name())["minutes"].sum().div(60).reindex(days)
    ```

**Check:** the sample listener peaks around 6 pm and listens about 45% more per day on weekends.

## Step 5: How does your listening change over time?

=== "R"

    ```r
    plays %>%
      mutate(week = floor_date(endTime, "week", week_start = 1)) %>%
      summarise(hours = sum(minutes) / 60, .by = week) %>%
      ggplot(aes(week, hours)) +
      geom_line(colour = "#0f766e", linewidth = 1) +
      labs(x = NULL, y = "Hours per week")
    ```

=== "Python"

    ```python
    weekly = plays.set_index("endTime")["minutes"].resample("W").sum() / 60
    weekly.plot(color="#0f766e", linewidth=2)
    plt.ylabel("Hours per week")
    plt.show()
    ```

Look for jumps. Exam weeks, holidays and summer jobs usually show up clearly.

## Step 6: Think like an economist

Economists trust what people **do** more than what they **say**. This idea is called *revealed preference*. Skipping a song is a choice you make without thinking, which makes it honest data about your taste.

=== "R"

    ```r
    df %>%
      summarise(plays = n(), skip_rate = mean(skipped), .by = artistName) %>%
      filter(plays >= 50) %>%
      arrange(desc(skip_rate))
    ```

=== "Python"

    ```python
    (
        df.groupby("artistName")
        .agg(plays=("skipped", "size"), skip_rate=("skipped", "mean"))
        .query("plays >= 50")
        .sort_values("skip_rate", ascending=False)
    )
    ```

The `plays >= 50` filter keeps only artists with enough plays to trust the rate. An artist you skipped once out of two plays has a 50% skip rate that means nothing.

**Check:** in the sample, the listener's favorite artists are skipped least. *Hysteresis* is skipped 45% of the time. Is that true for you?

## Go further

Pick one and try it on your own data.

1. **Your top artist each month.** Group by month and take the most-played artist. Does your favorite change?
2. **Binge sessions.** Find the day you listened the most. What were you doing?
3. **Discovery rate.** For each month, what share of plays were artists you had never played before?
4. **Night owl score.** What share of your listening happens between midnight and 5 am?
5. **Extended history.** Request **Extended streaming history** on the same Spotify page. It covers your whole account, back to the day you signed up, and takes up to 30 days. The column names differ: `ts` for the time, `master_metadata_album_artist_name` for the artist and `ms_played` for the milliseconds.

!!! warning "Your data, your choice"
    Your listening history is personal. Do not upload it to a public GitHub repository. If you share your analysis, share the charts, not the raw files.
