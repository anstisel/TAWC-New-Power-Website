<!-- Vue component for submitting replies to comments.
Upon admin approval, replies will be viewable by clicking "More" on the post page. -->

<template>
  <div class="container">
    <!-- Toggleable reply box with form to submit reply to backend for admin page.-->
    <b-button v-if="!isArchived" style="width: 90px" v-b-toggle="'reply-' + id" variant="primary">Reply</b-button>
    <b-collapse v-bind:id="'reply-' + id" class="mt-2">
      <b-card>
        <div class="col-lg-10">
          <div class="form__group">
            <textarea style="width: 500px; padding: 10px" v-model="newReply" rows="3" required cols="20"
              placeholder="Add a reply..." />
          </div>
        </div>
        <div style="margin-bottom: 10px" class="col-lg-2">
          <button @click="post_reply">Submit</button>
        </div>
        <!-- Error/Success Alerts (initially hidden) for validation with empty/filled inputs. -->
        <div v-bind:id="'empty-' + id" class="alert alert-danger" role="alert" hidden>
          <span class="glyphicon glyphicon-exclamation-sign"></span>
          <span class="sr-only">Error:</span>
          Please enter your reply.
        </div>
        <div v-bind:id="'valid-' + id" class="alert alert-success" role="alert" hidden>
          <span class="glyphicon glyphicon-exclamation-sign"></span>
          <span class="sr-only">Success!</span>
          Thank you for your reply! Your submission is currently awaiting
          approval from the administrator.
        </div>
      </b-card>
    </b-collapse>
  </div>
</template>

<script>
import { login_state } from "@/login_state.js";
import { useFetch } from "@/components/useFetch.vue";

// Function submits replies to admin for approval upon submit and validates for empty input boxes.
function post_reply() {
  if (this.newReply == "") {
    document.getElementById("empty-" + this.id).hidden = false;
    document.getElementById("valid-" + this.id).hidden = true;
  } else {
    document.getElementById("empty-" + this.id).hidden = true;
    document.getElementById("valid-" + this.id).hidden = false;
    // Submits reply content to admin if user is logged in, redirects to login on error.
    if (login_state.user_id) {
      this.submit_reply_api(login_state.user_id, this.newReply, "reply");
    } else {
      this.$auth0.loginWithRedirect();
    }
    this.newReply = "";
  }
}

// Initially defining props, methods, and variables to be updated with information from backend.
export default {
  name: "recursive-comment",
  props: {
    id: {
      type: Number,
      required: true,
    },
    isArchived: {
      type: Boolean,
      required: true,
    }
  },
  methods: {
    post_reply,
    // Function submits comment content, type (reply), parent comment, and post number to backend
    // to be rendered on admin page.
    submit_reply_api: function (author_id, body, type) {
      const requestOptions = {
        method: "POST",
        data: {
          body: body,
          type: type,
          parent_comment_id: this.id,
          post_id: this.post_id,
        },
      };
      // API call to POST reply information to backend database.
      useFetch("/api/comments", requestOptions, true);
    },
  },
  data() {
    return {
      newReply: "",
      login_state,
      post_id: this.$route.params.id,
    };
  },
};
</script>

<!-- Component-specific styling -->
<style scoped>
textarea {
  width: 100%;
  margin-top: 0.5em;
}
</style>
