<!-- Vue component for upvoting comments and updating backend with upvote information.
Also renders upvote count from backend and will save upvote counts and styling on page refresh. -->

<template>
  <span>
    <b-row>
      <b-col style="margin-right: 8px; margin-top:2px;" sm="1">
        <!-- Displays vote count with information from database. -->
        <span>{{ responsive_vote_count }}</span>
      </b-col>
      <b-col>
        <!-- Fills in upvote button upon click and submits. -->
        <b-button v-model:pressed="vote" @click="submit_upvote" variant="outline-warning">
          <fa icon="arrow-up" color="#083269" size="2xl" />
        </b-button>
      </b-col>
    </b-row>
  </span>
</template>

<script>
import { login_state } from "@/login_state.js";

// Function increments upvote count on frontend upon click and registers vote with backend database.
function submit_upvote() {
  this.vote = !this.vote;
  if (this.vote == true) {
    this.responsive_vote_count += 1;
  } else {
    this.responsive_vote_count -= 1;
  }
  // Upvotes if user is logged in, redirects to login otherwise.
  if (login_state.user_id) {
    submit_upvotes_api(this.comment_id, login_state.user_id);
  } else {
    this.$auth0.loginWithRedirect();
  }
}

// Function registers upvote with backend to be rendered responsively.
const submit_upvotes_api = function (comment_id, user_id) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  };
  // API call to POST upvote information to backend database.
  fetch(
    "/api/votes/comment/" + comment_id + "?user_id=" + user_id,
    requestOptions
  )
    .then((response) => response.json())
    .then((data) => console.log(data));
};

// Initially defining props, methods, and variables to be updated with information from backend.
export default {
  props: {
    vote_count: {
      type: Number,
      required: true,
    },
    comment_id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      login_state,
      vote: false,
      responsive_vote_count: this.vote_count,
    };
  },
  methods: {
    submit_upvote,
  },
  // Mounted function will run following code on initial page load.
  mounted() {
    const requestOptions = {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    };
    // API call to retrieve upvote count from database.
    fetch(
      "/api/votes/comment/" +
      this.comment_id +
      "?user_id=" +
      this.login_state.user_id,
      requestOptions
    )
      .then((response) => response.json())
      .then((data) => {
        // Verifies if user has already voted on the comment to save styling on frontend
        // and prevent multiple upvotes from one user.
        this.vote = data["voted_on_this_comment"];
      });
  },
};
</script>

<!-- Component-specific styling -->
<style scoped>
span {
  font-size: x-large;
  padding: 10px;
}
</style>
