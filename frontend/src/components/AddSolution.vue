<!-- Vue component for adding a new comment to a post.
The submitted comment will be sent to admin for approval and then rendered on the page upon approval. -->
<template>
  <b-form>
    <h3 style="text-align:left; margin-bottom:-2px;">Leave a...</h3>
    <b-form-select @click.prevent=" reset_form" style="width: 300px" v-model="type" :options="comment_types">
    </b-form-select>
    <b-row>
      <b-col col lg="10">
        <!-- Conditional rendering of comment input box based on type of comment. -->
        <div class="form__group">
          <textarea v-model="newSolution" rows="5" required cols="50" style="padding-left: 6px"
            v-if="this.type != 'other'" :placeholder="'Add a... ' + this.type" />
          <textarea v-model="newSolution" rows="5" required cols="50" style="padding-left: 6px" v-else
            :placeholder="'Add a... comment'" />
        </div>
        <!-- Error/Success Alerts (initially hidden) with conditional rendering based on comment type. -->
        <div class="alert alert-danger" role="alert" id="solutionEmptyAlert" hidden>
          <span class="sr-only">Error:</span>
          Please enter your
          <span v-if="this.type == 'solution'">solution.</span>
          <span v-else-if="this.type == 'clarification'">clarification.</span>
          <span v-else>comment.</span>
        </div>
        <div class="alert alert-success" role="alert" id="solutionSuccessAlert" hidden>
          <span class="sr-only">Success!</span>
          Thank you for your
          <span v-if="this.type == 'solution'">solution</span>
          <span v-else-if="this.type == 'clarification'">clarification</span>
          <span v-else-if="this.type == 'other'">comment</span>! Your
          submission is currently awaiting approval from the administrator.
        </div>
        <div class="alert alert-danger" role="alert" id="dropdownEmptyAlert" hidden>
          <span class="sr-only">Error:</span>
          Please select your comment type.
        </div>
      </b-col>
      <b-col col lg="2">
        <button id="submit" @click.prevent="post_solution">Submit</button>
      </b-col>
    </b-row>
  </b-form>
</template>

<script>
import { login_state } from "@/login_state.js";
import { useFetch } from "@/components/useFetch.vue";

// Function submits comments to admin for approval upon submit and validates for empty input boxes
function post_solution() {
  if (this.newSolution == "" && this.type != "") {
    document.getElementById("solutionEmptyAlert").hidden = false;
    document.getElementById("solutionSuccessAlert").hidden = true;
    document.getElementById("dropdownEmptyAlert").hidden = true;
  } else if (this.type == "") {
    document.getElementById("solutionEmptyAlert").hidden = true;
    document.getElementById("solutionSuccessAlert").hidden = true;
    document.getElementById("dropdownEmptyAlert").hidden = false;
  } else {
    document.getElementById("solutionEmptyAlert").hidden = true;
    document.getElementById("solutionSuccessAlert").hidden = false;
    document.getElementById("dropdownEmptyAlert").hidden = true;
    // Submits comment content to admin if user is logged in, redirects to login on error.
    if (login_state.user_id) {
      submit_comment_api(
        login_state.user_id,
        this.newSolution,
        this.type,
        this.post_id
      );
    } else {
      this.$auth0.loginWithRedirect();
    }
    this.newSolution = "";
  }
}
// Resets error when user selects a different comment type.
function reset_form() {
  document.getElementById("solutionEmptyAlert").hidden = true;
  document.getElementById("solutionSuccessAlert").hidden = true;
  document.getElementById("dropdownEmptyAlert").hidden = true;
}

// Function to submit comment content, type, post, and user_id to backend to be rendered on admin page.
const submit_comment_api = function (author_id, body, type, post_id) {
  const requestOptions = {
    method: "POST",
    data: {
      author_id: author_id,
      body: body,
      type: type,
      post_id: post_id,
    },
  };
  // API call to POST comment information to backend database.
  useFetch("/api/comments", requestOptions, true);
};

// Initially defining props, methods, and variables to be updated with information from backend.
export default {
  props: {
    post_id: {
      type: Number,
    },
  },
  data() {
    return {
      type: "",
      newSolution: "",
      login_state,
      comment_types: [
        { value: "", text: "Please select your comment type." },
        { value: "solution", text: "Solution" },
        { value: "clarification", text: "Clarification" },
        { value: "other", text: "Other" },
      ],
    };
  },
  methods: {
    post_solution,
    reset_form,
  },
};
</script>

<!-- Component-specific styling -->
<style scoped>
label {
  display: block;
  margin-bottom: 1em;
  font-weight: 700;
  font-family: Padauk, sans-serif;
}

textarea {
  width: 100%;
  margin-top: 0.5em;
}

button {
  border: unset;
  background: #020b5e;
  color: #d17d1d;
  font-weight: 700;
  padding: 1em 2.5em;
  margin-top: 2.5em;
}
</style>
