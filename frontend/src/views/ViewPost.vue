<!-- View for viewing all components of a New Power post or discussion.
Renders post title, content, author, submission box for new comments, 
and three types of comments depending on whether the user has made a contribution to the post. -->

<template>
  <div class="container main-content" style="padding-bottom: 150px">
    <br />
    <h1>{{ this.post.title }}</h1>
    <h3>{{ this.post.creator_username }}</h3>
    <p>{{ this.post.body }}</p>
    <div v-if="!this.post.archived">
      <br />
      <hr />
      <!-- Inserting component to submit new comments. -->
      <add-solution v-bind=" { post_id: this.post_num, }" />
    </div>
    <br />
    <hr />
    <!-- Below div will only display if user is logged in and has contributed to view comments. -->
    <div v-if="this.participation_check == true">
      <b-tabs content-class="mt-3">
        <b-tab title="Solutions" title-link-class="tab-title">
          <!-- Rendering comments based on comment type displaying comment body, collapsible replies,
             comment author, and vote_count. -->
          <div v-for="(item, index) in comments.solutions" :key="index" class="comments">
            <PostComment v-bind="{
              comment_id: item.comment_id,
              author_id: item.author_id,
              body: item.body,
              replies: item.replies,
              creator_username: item.creator_username,
              vote_count: item.vote_count,
              archived: this.post.archived,
            }" />
            <hr />
          </div>
        </b-tab>
        <b-tab title="Clarifications" title-link-class="tab-title">
          <div v-for="(item, index) in comments.clarifications" :key="index" class="comments">
            <PostComment v-bind="{
              comment_id: item.comment_id,
              author_id: item.author_id,
              body: item.body,
              replies: item.replies,
              creator_username: item.creator_username,
              vote_count: item.vote_count,
              archived: this.post.archived,
            }" />
            <hr />
          </div>
        </b-tab>
        <b-tab title="Other" title-link-class="tab-title">
          <div v-for="(item, index) in comments.other" :key="index" class="comments">
            <PostComment v-bind="{
              comment_id: item.comment_id,
              author_id: item.author_id,
              body: item.body,
              replies: item.replies,
              creator_username: item.creator_username,
              vote_count: item.vote_count,
              archived: this.post.archived,
            }" />
            <hr />
          </div>
        </b-tab>
      </b-tabs>
    </div>
    <!-- Message that is displayed if user has not participated in the discussion. -->
    <div v-else>
      <h2 class="participation_alert">
        Please make a comment contribution to see the rest of the comments.
      </h2>
    </div>
  </div>
</template>

<script>
import AddSolution from "@/components/AddSolution.vue";
import PostComment from "@/components/PostComment.vue";
import { login_state } from "../login_state";

// Initially defining props and variables to be updated with information from child components and backend.
export default {
  props: {
    vote_count: {
      type: Number,
    },
    comment_id: {
      type: Number,
    },
  },
  data() {
    return {
      comments: {},
      post: [],
      participation_check: false,
      login_state,
      isAuthenticated: this.$auth0.isAuthenticated,
      post_num: Number(this.$route.params.id),
    };
  },
  components: {
    AddSolution,
    PostComment,
  },
  // Mounted function will run following code on initial page load.
  mounted() {
    // If user is not logged in, will redirect to login page.
    if (!this.isAuthenticated) {
      this.$auth0.loginWithRedirect();
    }
    // Fetch post details.
    const post_num = String(this.$route.params.id);
    const requestOptions = {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    };
    // Fetching post information from backend database.
    fetch("/api/posts/" + post_num, requestOptions)
      .then((response) => response.json())
      .then((data) => {
        console.log("Fetched!");
        this.post = data;
      });
    // Fetching all three types of approved comments from backend database.
    fetch(
      "/api/comments/approved/" + post_num + "?type=solution",
      requestOptions
    )
      .then((response) => response.json())
      .then((data) => {
        this.comments["solutions"] = data["items"];
        console.log(this.comments);
      });
    fetch(
      "/api/comments/approved/" + post_num + "?type=clarification",
      requestOptions
    )
      .then((response) => response.json())
      .then((data) => {
        this.comments["clarifications"] = data["items"];
        console.log(this.comments);
      });
    fetch("/api/comments/approved/" + post_num + "?type=other", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.comments["other"] = data["items"];
        console.log(this.comments);
      });
    // Fetching participation check for logged in user to determine access to comments.
    fetch(
      "/api/posts/check/" + post_num + "?user_id=" + login_state.user_id,
      requestOptions
    )
      .then((response) => response.json())
      .then((data) => {
        this.participation_check = data["participation_check"];
        console.log(this.participation_check);
      });
  },
};
</script>

<!-- Page-specific styling for ViewPost view. -->
<style>
.comments ul {
  padding-left: 16px;
  margin: 6px 0;
  border-left: dotted;
  border-color: navy;
}

.main-content {
  color: darkslategray;
}

.participation_alert {
  color: #696969;
  text-align: center;
  margin-top: 5%;
}
</style>
