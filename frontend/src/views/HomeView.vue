<template>
  <div>
    <img
      class="background-img centre"
      src="@/assets/background2.png"
      style="height: 250px"
    />

    <!-- Central Container Text -->
    <div class="msg centre" id="title-text">
      <h1>Welcome to TAWC Power Room</h1>
      <p>Have your say!</p>
      <p>Get involved and improve animal welfare together!</p>
    </div>

    <!-- Input Further Text Here! -->
    <div class="text centre">
      <p>
        TAWC Power Room is a participatory and peer-driven online platform,
        built for the animals.
      </p>
      <p>Click to participate and have your say below:</p>
      <b-row>
        <b-col>
          <!-- Buttons to submit a post and go to discussion board -->
          <b-button-group>
            <router-link to="/discussion-board">
              <b-button
                size="lg"
                id="discussionboard_link"
                class="button_style"
              >
                Discussion Board
              </b-button>
            </router-link>
            <div v-if="isAuthenticated">
              <router-link to="/submit-post/">
                <b-button size="lg" id="submitpost_link" class="button_style">
                  Submit a Question!
                </b-button>
              </router-link>
            </div>
            <div v-else>
              <!-- Button trigger modal -->
              <b-button
                class="btn btn-primary button_style"
                data-bs-toggle="modal"
                data-bs-target="#exampleModal"
                size="lg"

                id="submitpost_link"
              >
                Submit a Question!
              </b-button>
              <!-- Modal -->
              <div
                class="modal fade"
                id="exampleModal"
                tabindex="-1"
                aria-labelledby="exampleModalLabel"
                aria-hidden="true"
              >
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="exampleModalLabel">Log In</h5>
                      <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                      ></button>

                    </div>
                    <div class="modal-body">
                      You are not logged into an account. <br />If you would
                      like to view this post please log in first.
                    </div>
                    <div class="modal-footer">
                      <b-button
                        id="close_button"
                        type="button"
                        class="btn btn-secondary"
                        data-bs-dismiss="modal"
                        >Close</b-button
                      >
                      <b-button id="login_button" @click="login">
                        Log In
                      </b-button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </b-button-group>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import { login_state } from "@/login_state.js";

export default {
  data() {
    return {
      login_state,
      user: this.$auth0.user,
      isAuthenticated: this.$auth0.isAuthenticated,
    };
  },
  methods: {
    login() {
      this.$auth0.loginWithRedirect();
    },
  },
};
</script>

<style scoped>
/*css page for he index page*/
body {
  background-color: #edf4f6;
  margin: 0%;
  font-family: Arial, Helvetica, sans-serif;
}

.background-img {
  position: relative;
  width: 100%;
  height: 100%;
  z-index: -10;
}

.centre {
  display: block;
  margin-left: auto;
  margin-right: auto;
}

@media screen and (min-width: 1200px) {
  .background-img {
    width: 75%;
    height: 75%;
  }
}

.msg {
  background-color: #083269;
  width: fit-content;
  height: fit-content;
  padding: 20px 100px;
  margin-top: -75px;
  text-align: center;
  font-size: 30px;
}

.msg h1 {
  color: #f9ae42;
}

.msg p {
  color: #ffffff;
}

.text {
  width: fit-content;
  height: fit-content;
  text-align: center;
}

.text p {
  color: #192024;
  padding: 20px;
  font-size: 30px;
}

.button_style {
  border-radius: 10px;
  width: fit-content;
  height: fit-content;
  font-size: 30px;
  text-align: center;
  color: #ffffff;
  padding: 20px 30px;
  border: none;
  margin-bottom: 20px;
}
</style>
