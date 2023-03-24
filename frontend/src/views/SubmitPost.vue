<!-- View for submitting a new question or post to be displayed on the discussion board 
upon admin approval. -->

<template>
  <!-- Submission boxes for post title and description, submit on button click -->
  <h1 class="jumbotron text-center">Submit your post here!</h1>
  <b-container style="width: 60%; padding: 20px">
    <b-form @submit.prevent="submit_post">
      <h2 style="margin-bottom: 12px">Please enter your post title here:</h2>
      <b-col>
        <b-form-input v-model="title" id="title" size="lg" placeholder="Enter your post title here">
        </b-form-input>
        <br />
      </b-col>
      <h2 style="margin-bottom: 12px">Please enter your post description:</h2>
      <b-col>
        <b-form-textarea v-model="body" id="desc" size="lg" rows="4" placeholder="Enter your description here">
        </b-form-textarea>
        <br />
      </b-col>
      <input class="submit" type="submit" value="Submit" />
    </b-form>
  </b-container>
  <br />
  <!-- Error/Success Alerts (initially hidden) for validation with empty/filled inputs. -->
  <div class="alert alert-danger" role="alert" id="postEmptyAlert" hidden>
    <span class="glyphicon glyphicon-exclamation-sign"></span>
    <span class="sr-only">Error:</span>
    Invalid input!
  </div>
  <div class="alert alert-success" role="alert" id="postSuccessAlert" hidden>
    <span class="glyphicon glyphicon-exclamation-sign"></span>
    <span class="sr-only">Success!</span>
    Thank you for posting a question! Your question is currently awaiting
    approval from the administrator.
  </div>
</template>

<script>
import { login_state } from "@/login_state.js";
import { useFetch } from "@/components/useFetch.vue";

// Function submits new discussion questions to admin for approval upon submit
// and validates for empty input boxes.
function submit_post() {
  if (this.title == "" || this.body == "") {
    document.getElementById("postEmptyAlert").hidden = false;
    document.getElementById("postSuccessAlert").hidden = true;
  } else {
    document.getElementById("postEmptyAlert").hidden = true;
    document.getElementById("postSuccessAlert").hidden = false;
    // Submits discussion post content to admin if user is logged in, redirects to login on error.
    if (login_state.user_id) {
      submit_post_api(login_state.user_id, this.title, this.body);
    } else {
      this.$auth0.loginWithRedirect();
    }
    this.title = "";
    this.body = "";
  }
}

// Function submits post title and content to backend to be rendered on admin page.
const submit_post_api = function (creator_id, title, body) {
  const config = {
    method: "POST",
    data: {
      body: body,
      title: title,
    },
  };
  // API call to POST post information to backend database.
  useFetch("/api/posts", config, true);
  console.log("sent");
};

// Initially defining props, methods, and variables to be updated with information from backend.
export default {
  methods: {
    submit_post,
    submit_post_api,
    useFetch,
  },
  data() {
    return {
      login_state,
      title: "",
      body: "",
      isAuthenticated: this.$auth0.isAuthenticated,
    };
  },
  // Mounted function will run following code on initial page load.
  // Redirects to login page if user is not authenticated.
  mounted() {
    if (!this.isAuthenticated) {
      this.$auth0.loginWithRedirect();
    }
  },
};
</script>

<!-- Page-specific styling for SubmitPost view. -->
<style scoped>
.submit {
  width: fit-content;
  padding: 8px 15px;
  color: #083269;
  background-color: white;
  font-size: large;
  font-weight: 500;
  border: 3px solid #f9ae42;
  border-radius: 5px;
}

.submit:hover {
  background-color: #f9ae42;
}

.submit:active {
  border-color: #fb9e1c;
  background-color: #fb9e1c;
}

.alert {
  width: 60%;
  margin:auto;
}
</style>
