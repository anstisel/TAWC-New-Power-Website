<template>
  <div>
    <div
      class="container-fluid px-lg-4 px-xl-5 contentDiv"
      style="padding: 50px"
    >
      <div class="row">
        <div class="col-lg-4">
          <b-card header="header">
            <template #header>
              <h2 class="card-heading">My Profile</h2>
            </template>
            <!--------- Profile Section ---------------->
            <b-card-body>
              <b-img
                :src="login_state.avatar"
                fluid
                alt="Profile picture not loaded"
                center
              ></b-img>
              <h2 class="mb-3" style="padding: 20px 0px 0px 0px">
                {{ login_state.username }}
              </h2>
            </b-card-body>
          </b-card>
          <br />
        </div>

        <!------------ My Posts Section ----------->
        <!-- My Post Heading -->
        <div class="col-lg-8">
          <b-card no-body header="header">
            <template #header>
              <h2 class="card-heading">My Posts</h2>
            </template>
            <h2 v-if="posts.length === 0">You have no posts yet!</h2>

            <b-card-group deck>
              <b-container fluid>
                <b-row>
                  <b-col
                    cols="lg-12"
                    v-for="post in posts"
                    :key="post.post_id"
                    style="padding: 10px 20px 30px 20px"
                  >
                    <APost
                      v-bind="{
                        title: post.title,
                        details: post.body,
                        username: post.creator_username,
                        date: post.create_time,
                        id: post.post_id,
                        approved: post.approved,
                        last_moderate_time: post.last_moderate_time,
                        on_profile: true,
                        admin_msg: post.admin_msg,
                      }"
                    />
                  </b-col>
                </b-row>
                <b-pagination
                  v-model="currentPage"
                  :total-rows="rows"
                  :per-page="perPage"
                  align="center"
                  size="lg"
                ></b-pagination>
              </b-container>
            </b-card-group>
          </b-card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { login_state } from "@/login_state.js";
import APost from "@/components/APost.vue";

export default {
  components: {
    APost,
  },
  data() {
    return {
      login_state,
      posts: [],
      perPage: 1,
      currentPage: 1,
      total_pages: 1,
      isAuthenticated: this.$auth0.isAuthenticated,
    };
  },
  computed: {
    rows() {
      return this.total_pages;
    },
  },
  watch: {
    currentPage: function () {
      const userid = this.login_state.user_id;

      const requestOptions = {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      };
      //      "/api/posts/approved?page=" + this.currentPage + "&per_page=1",
      fetch(
        "/api/posts/user/" +
          userid +
          "?page=" +
          this.currentPage +
          "&per_page=6",
        requestOptions
      )
        .then((response) => response.json())
        .then((data) => {
          this.posts = data["items"];
        });
    },
  },
  mounted() {
    if (!this.isAuthenticated) {
      this.$auth0.loginWithRedirect();
    }

    const userid = this.login_state.user_id;

    const requestOptions = {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    };

    fetch("/api/posts/user/" + userid + "?page=1&per_page=6", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.posts = data["items"];
        this.total_pages = data._meta["total_pages"];
      });
  },
};
</script>
