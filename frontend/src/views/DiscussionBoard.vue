<template>
  <div>
    <!-- Title and Sub-title -->
    <h1 id="discussion-title">Discussion Threads</h1>
    <h3 id="subtitle">TAWC Approved</h3>
    <div style="padding: 0px 50px 50px 50px">
      <b-tabs align="left" class="discussiontabs">
        <!-- Popular Tab with Posts -->
        <b-tab title="Popular">
          <b-card-group deck>
            <b-container fluid>
              <div class="row" style="padding: 20px">
                <div
                  class="col-md-4"
                  md="auto"
                  v-for="post in posts"
                  :key="post.post_id"
                  style="padding: 0px 20px 30px 0px"
                >
                  <APost
                    v-bind="{
                      title: post.title,
                      details: post.body,
                      username: post.creator_username,
                      date: post.create_time,
                      id: post.post_id,
                      perPage: perPage,
                    }"
                  />
                </div>
              </div>

              <b-pagination
                v-model="currentPage"
                :total-rows="rows"
                :per-page="perPage"
                align="center"
                size="lg"
              ></b-pagination>
            </b-container>
          </b-card-group>
        </b-tab>

        <!--Archived Tab with Posts -->
        <b-tab title="Archived">
          <b-card-group deck>
            <b-container fluid>
              <div class="row" style="padding: 10px">
                <div
                  class="col-md-4"
                  md="auto"
                  v-for="post in archived"
                  :key="post.post_id"
                  style="padding: 0px 20px 30px 0px"
                >
                  <APost
                    id="a-post"
                    v-bind="{
                      title: post.title,
                      details: post.body,
                      username: post.creator_username,
                      date: post.create_time,
                      id: post.post_id,
                    }"
                  />
                </div>
              </div>
              <b-pagination
                v-model="archivedcurrentPage"
                :total-rows="archivedrows"
                :per-page="archivedperPage"
                align="center"
                size="lg"
              ></b-pagination>
            </b-container>
          </b-card-group>
        </b-tab>
      </b-tabs>
    </div>
  </div>
</template>

<script>
import APost from "@/components/APost.vue";

export default {
  name: "discussion-board",
  components: {
    APost,
  },
  data() {
    return {
      perPage: 1,
      archivedperPage: 1,
      currentPage: 1,
      archivedcurrentPage: 1,
      posts: [],
      archived: [],
      total_pages: 1,
      total_pages_archived: 1,
    };
  },

  computed: {
    rows() {
      return this.total_pages; // return this.posts.length;
    },
    archivedrows() {
      return this.total_pages_archived;
    },
  },
  watch: {
    currentPage: function () {
      const requestOptions = {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      };
      //      "/api/posts/approved?page=" + this.currentPage + "&per_page=1",
      fetch(
        "/api/posts/approved?page=" + this.currentPage + "&per_page=12",
        requestOptions
      )
        .then((response) => response.json())
        .then((data) => {
          this.posts = data["items"];
        });
    },
    archivedcurrentPage: function () {
      const requestOptions = {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      };
      //      "/api/posts/approved?page=" + this.currentPage + "&per_page=1",
      fetch(
        "/api/posts/approved/archived?page=" +
          this.archivedcurrentPage +
          "&per_page=12",
        requestOptions
      )
        .then((response) => response.json())
        .then((data) => {
          this.archived = data["items"];
        });
    },
  },
  mounted() {
    const requestOptions = {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    };
    //      "/api/posts/approved?page=" + this.currentPage + "&per_page=1",

    fetch("/api/posts/approved?page=1&per_page=12", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.posts = data["items"];
        this.total_pages = data._meta["total_pages"];
      });

    fetch("/api/posts/approved/archived?page=1&per_page=12", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.archived = data["items"];
        this.total_pages_archived = data._meta["total_pages"];
      });
  },
};
</script>
