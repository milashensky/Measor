$().ready(function() {
    Vue.use(VueResource);
    Vue.component('log-status', {
        props: ['slug', 'name'],
        template: `
            <div>
                <span v-if="ready" :class="(status? 'text-success': 'text-danger')">
                    {{(status? 'Success': 'Failed')}}
                </span>
            </div>
        `,
        data: function(){
            return {
                status: false,
                ready: false,
            }
        },
        computed: {
            resource: function () {
                return this.$resource('/api/{slug}/log/{log_name}/status');
            },
        },
        methods: {
            getStatus: function(slug, log_name) {
                this.resource.get({'slug': slug, 'log_name': log_name}).then(function(response) {
                    this.status = response.body.status
                    this.ready = true
                },function () {
                    this.ready = true
                    return false;
                });
            },
        },
        created: function(){
            let vm = this;
            vm.getStatus(vm.slug, vm.name)
        }
    });
    new Vue({
        el: '#logs',
    })
});
