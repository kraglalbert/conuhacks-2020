<template>
    <div>
        <div class="text-h4 q-mb " >{{event.name}}</div>
        <p>{{event.date_time}}</p>
        <q-badge class="primary">{{event.category}}</q-badge>
            <p>{{event.description}}</p>
        <q-separator />
    </div>
</template>

<script>
import moment from "moment";

export default {
  name: 'CalendarItemList',
  props: {
    event: Object
  }
}
</script>