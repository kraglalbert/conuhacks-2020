<template>
  <q-card>
    <q-card-section class="row items-center">
      <div class="text-h6">Add New Transaction</div>
      <q-space />
      <q-btn icon="close" flat round dense v-close-popup />
    </q-card-section>

    <q-card-section>
      <q-form @submit="createTransaction" class="q-gutter-sm">
        <q-input
          filled
          v-model="transactionTitle"
          label="Transaction Title"
          lazy-rules
          :rules="[
            val => (val && val.length > 0) || 'Please enter a transaction title'
          ]"
        />

        <q-input
          filled
          v-model="transactionSource"
          label="Source"
          lazy-rules
          :rules="[val => (val && val.length > 0) || 'Please enter a source']"
        />

        <q-input
          filled
          v-model="transactionAmount"
          label="Amount"
          mask="#.##"
          fill-mask="0"
          reverse-fill-mask
          prefix="$"
          lazy-rules
          :rules="[
            val =>
              (val !== null && val !== '') ||
              'Please enter the transaction amount',
            val => val > 0 || 'Amount cannot be negative or zero'
          ]"
        />

        <div>
          <q-btn-toggle
            v-model="transactionType"
            class="my-custom-toggle"
            no-caps
            unelevated
            toggle-color="primary"
            color="white"
            text-color="primary"
            :options="[
              { label: 'Spending', value: 'spending' },
              { label: 'Profit', value: 'profit' }
            ]"
          />
        </div>

        <q-input filled v-model="transactionDate" mask="date" :rules="['date']">
          <template v-slot:append>
            <q-icon name="event" class="cursor-pointer">
              <q-popup-proxy
                ref="qDateProxy"
                transition-show="scale"
                transition-hide="scale"
              >
                <q-date
                  v-model="transactionDate"
                  @input="() => $refs.qDateProxy.hide()"
                />
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>

        <q-btn color="primary" type="submit" label="Add" />
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script>
import moment from "moment";
export default {
  name: "HomeNewTransactionPopup",
  data() {
    return {
      transactionType: "spending",
      transactionDate: moment(new Date()).format("YYYY/MM/DD"),
      transactionTitle: "",
      transactionSource: "",
      transactionAmount: ""
    };
  },
  methods: {
    createTransaction: function() {
      const user = this.$store.state.currentUser;
      let amount = parseFloat(this.transactionAmount) * 100;
      if (this.transactionType === "spending") {
        amount = amount * -1;
      }
      const date = new Date(this.transactionDate);
      const data = {
        title: this.transactionTitle,
        source: this.transactionSource,
        amount: amount,
        email: user.email,
        year: date.getFullYear(),
        month: date.getUTCMonth() + 1,
        day: date.getUTCDate()
      };
      this.$axios
        .post("/transactions/create", data, {
          headers: {
            Authorization: this.$store.state.token
          }
        })
        .then(_resp => {
          this.$q.notify({
            color: "green-4",
            position: "top",
            textColor: "white",
            icon: "cloud_done",
            message: "Transaction Added Successfully"
          });
          // let parent know to close the dialog
          this.$emit("dialog-closed");
        })
        .catch(_err => {
          this.$q.notify({
            color: "red-4",
            position: "top",
            textColor: "white",
            icon: "error",
            message: "Something went wrong, please try again"
          });
        });
    }
  }
};
</script>
