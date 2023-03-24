<!-- Vue component for rendering posts on the Discussion Board view. -->

<template>
  <b-card v-show="active" id="post-card" no-body header-tag="header" class="card h-100 flex-column">
    <!-- Title of Cards -->
    <template #header>
      <h2 id="cardheader">{{ title }}</h2>
    </template>
    <b-card-body class="d-flex flex-column">
      <!-- Dropdown for delete feature -->
      <b-dropdown v-if="on_profile" no-caret variant="no-outline" style="position: absolute; right: 20px">
        <template #button-content>
          <fa icon="ellipsis-vertical" color="#083269" size="xl" />
        </template>
        <b-dropdown-item-button @click="del">Delete</b-dropdown-item-button>
      </b-dropdown>

      <!-- Submission's details - username, date, description -->
      <b-card-text class="subtitle"> {{ username }} </b-card-text>
      <b-card-text> {{ date }} </b-card-text>
      <b-card-text style="text-align: justify">
        <!-- Shortens description content if greater than 500 characters. -->
        <span v-if="details.length > 500">
          {{ details.slice(0, 500) }}...
        </span>
        <span v-else> {{ details }} </span>
      </b-card-text>

      <!-- Rejected/Accepted/Waiting status for profile page -->
      <div v-if="on_profile">
        <div v-if="last_moderate_time == 'None'" id="waitingstatus">
          Waiting for admin approval!
        </div>
        <div v-else-if="approved" id="approvedstatus">Approved!</div>
        <div v-else-if="!approved" id="unapprovedstatus">
          Rejected!
          <div v-if="admin_msg">Reasoning: {{ admin_msg }}</div>
        </div>
      </div>

      <!-- Button routes to post if User is authenticated -->
      <div v-if="isAuthenticated" class="bottom">
        <b-button id="to_post" type="button" style="width: 100%" :to="'/view-post/' + id">
          Go to post!
        </b-button>
      </div>
      <div v-else class="bottom">
        <!-- Button trigger modal (Opens must-login popup) -->

        <b-button id="to_post" style="width: 100%" data-bs-toggle="modal" :data-bs-target="'#Modal' + id">
          Go to post!
        </b-button>

        <!-- Modal -->
        <div class="modal fade" :id="'Modal' + id" tabindex="-1" aria-labelledby="ModalLabel" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="ModalLabel">Log In</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                You are not logged into an account. <br />If you would like to
                view this post please log in first.
              </div>
              <div class="modal-footer">
                <button id="close_button" type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                  Close
                </button>
                <b-button id="login_button" @click="login"> Log In </b-button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Button for linking to post -->
      <!-- <b-button
          class="mt-auto"
          href="#"
          variant="primary"
          :to="'/view-post/' + id"
        >
          Go to post!
        </b-button>-->
    </b-card-body>
  </b-card>
</template>

<script>
import { useFetch } from "@/components/useFetch.vue";

export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    details: {
      type: String,
      required: true,
    },
    username: {
      type: String,
      required: true,
    },
    date: {},
    id: {},
    approved: {},
    last_moderate_time: {},
    on_profile: { default: false },
    admin_msg: {},
  },
  data() {
    return {
      isAuthenticated: this.$auth0.isAuthenticated,
      active: true,
    };
  },
  methods: {
    login() {
      this.$auth0.loginWithRedirect();
    },
    del() {
      const config = {
        method: "PUT",
      };
      this.active = false;
      useFetch("/api/posts/user/delete/" + this.id, config, true);
    },
  },
};
</script>

<style scoped>
.card {
  background-color: rgba(255, 255, 255, 0.927);
  margin: 10px 10px 10px 10px;
}

.row {
  margin: 15px 10px 20px 10px;
}

.bottom {
  margin-top: auto;
}
</style>
