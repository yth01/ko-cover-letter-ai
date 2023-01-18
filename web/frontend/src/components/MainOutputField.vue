<template>
    <div id="output-field">
        <div v-for="analyzedResult in analyzedResults" v-bind:key="analyzedResult">{{ analyzedResult }}</div>
    </div>
</template>

<script>
export default {
    created() {
        this.$EventBus.$on('analyzedResults', (analyzedResults) => {
            console.log(analyzedResults);
            console.log("passed!!!");
            this.analyzedResults = analyzedResults
        })
    },
    data: function () {
        return {
            analyzedResults: [],
        }
    },
}
</script>

<style scoped>
#output-field {
    /* Auto layout */
    display: flex;
    flex-direction: column;
    align-items: center;

    margin: 20px 0px;
}

div {
    margin: 10px 0px;
}
</style>