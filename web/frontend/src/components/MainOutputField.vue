<template>
    <div id="output-field">
        <li id="output-field-content" v-for="analyzedResult in analyzedResults" v-bind:key="analyzedResult">
            {{ analyzedResult }}
        </li>
    </div>
</template>

<script>
export default {
    created() {
        this.$EventBus.$on('clearOutput', () => {
            this.analyzedResults = []
        }),
        this.$EventBus.$on('analyzedResults', (analyzedResults) => {
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
    margin: 0% 14%;
}

#output-field-content{
    background: #FAFAFA;
    border: 1.5px solid #1976D2;
    border-radius: 5px;
    padding: 10px 20px;
    width: 100%;
    margin-bottom: 1%;
}

</style>