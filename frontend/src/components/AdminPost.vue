<template>
  <div v-show="active">
    <b-card>
      <!-- Submission's status (approved/rejeted) - only shows under History tab -->
      <span
        class="status"
        v-if="reactive_approved"
        style="background-color: seagreen"
      >
        Approved
      </span>
      <span
        class="status"
        v-if="reactive_approved == false"
        style="background-color: crimson"
      >
        Rejected
      </span>

      <!-- Dropdown for actions: Delete, Change status, Archive/Unarchive -->
      <b-dropdown
        no-caret
        variant="no-outline"
        style="position: absolute; right: 20px"
      >
        <template #button-content>
          <fa icon="ellipsis-vertical" color="#083269" size="xl" />
        </template>
        <b-dropdown-item-button @click="del">Delete</b-dropdown-item-button>
        <b-dropdown-item-button v-if="history" @click="change_stat"
          >Change status</b-dropdown-item-button
        >
        <b-dropdown-item-button
          v-if="approved == true && archived == false"
          @click="archive"
        >
          Archive
        </b-dropdown-item-button>
        <b-dropdown-item-button v-if="archived" @click="unarchive">
          Unarchive
        </b-dropdown-item-button>
      </b-dropdown>

      <!-- Submission's details - title, user's avatar and name, date submitted, description -->
      <div style="font-size: 30px; padding: 0pt 20pt">

        <router-link :to="'/view-post/' + pid" style="text-decoration: none">
          {{ this.post_title }}

        </router-link>
      </div>
      <b-row>
        <b-list-group-item class="d-flex align-items-center">
          <img :src="avatar" style="width: 60px; height: 60px" />
          <span class="mr-auto">
            &nbsp;&nbsp; {{ username }} &nbsp;&nbsp; {{ date }}
          </span>
        </b-list-group-item>
      </b-row>
      <!-- Shortens description content if greater than 500 characters. -->
      <b-row>
        <span v-if="details.length > 500">
          {{ details.slice(0, 500) }}...
        </span>
        <span v-else> {{ details }} </span>
      </b-row>

      <!-- Accept/Reject actions, textbox for optional admin message - hidden in History tab -->
      <b-button-group v-if="history == false">
        <b-button id="approve" @click="approve" variant="success"
          >Approve</b-button
        >
        <b-button id="reject" @click="reject" variant="danger">Reject</b-button>
      </b-button-group>
      <b-row v-if="history == false">
        Optional message:
        <input
          type="text"
          v-model="message"
          placeholder="Type the reason here..."
          style="
            border-radius: 5px;
            border: 1px solid #083269;
            padding: 5px 10px;
          "
        />
      </b-row>
    </b-card>
  </div>
</template>

<script>
import { useFetch } from "@/components/useFetch.vue";

export default {
  data() {
    return {
      message: "",
      active: true,
      post_title: "",
      reactive_approved: this.approved,
    };
  },
  props: {
    id: { required: true },
    pid: { required: true },
    title: { required: false },
    username: { type: String, required: true },
    avatar: { type: String, default: "http://www.gravatar.com/avatar/?d=mp" },
    date: {},
    details: { type: String, required: true },
    approved: {},
    archived: {},
    history: { default: false },
    comment: { default: true },
  },
  mounted() {
    if (this.comment) {
      const requestOptions = {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      };
      fetch("/api/posts/" + this.pid, requestOptions)
        .then((response) => response.json())
        .then((data) => {
          this.post_title = data["title"];
        });
    } else {
      this.post_title = this.title;
    }
  },
  methods: {
    del() {
      const config = {
        method: "PUT",
      };
      this.active = false;
      if (this.comment) {
        useFetch("/api/comments/admin/delete/" + this.id, config, true);
      } else {
        useFetch("/api/posts/admin/delete/" + this.id, config, true);
      }
    },
    change_stat() {
      if (this.reactive_approved) {
        this.reject();
        this.reactive_approved = false;
        console.log(this.reactive_approved);
      } else {
        this.approve();
        this.reactive_approved = true;
        console.log(this.reactive_approved);
      }
    },
    archive() {
      const config = {
        method: "PUT",
        data: { archived: true },
      };
      useFetch("/api/posts/admin/archive/" + this.id, config, true);
    },
    unarchive() {
      const config = {
        method: "PUT",
        data: { archived: false },
      };
      useFetch("/api/posts/admin/archive/" + this.id, config, true);
    },
    approve_or_reject(approved) {
      if (!this.history) {
        this.active = false;
      }
      const config = {
        method: "PUT",
        data: {
          approved: approved,
          admin_msg: this.message,
        },
      };
      if (this.comment) {
        useFetch("/api/comments/admin/" + this.id, config, true);
      } else {
        useFetch("/api/posts/admin/" + this.id, config, true);
      }
    },
    approve() {
      this.approve_or_reject(true);
    },
    reject() {
      this.approve_or_reject(false);
    },
  },
};
</script>

<style scoped>
.card {
  background-color: rgba(255, 255, 255, 0.927);
  margin: 20px;
  padding: 5pt;
}

.row {
  margin: 10px 20px;
}

button {
  width: 90px;
  margin: 15px 10px 0px 20px;
}

input {
  margin: 5px auto 0px;
}

.status {
  position: absolute;
  right: 70px;
  padding: 6px 20px;
  border-radius: 5px;
  font-size: large;
  color: white;
}
</style>
