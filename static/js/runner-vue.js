$().ready(function() {
    Vue.use(VueResource);
    new Vue({
        el: '#dashboard',
        data: {
            tasks: [],
            running: false,
            apiUrl: '/api/task/',
            checkInterval: 10,
            interval: {}
        },
        computed: {
            resource: function () {
                return this.$resource(this.apiUrl + '{slug}');
            },
        },
        created: function() {
            let vm = this;
            vm.resource.get().then(function(response) {
                this.tasks = response.body;
            },function () {});
            vm.interval = setInterval(function () {
                vm.resource.get().then(function(response) {
                    this.tasks = response.body;
                },function () {})
            }, 1000 * vm.checkInterval);
            setTimeout(function () {
                $('[tooltip]').each(function(t, el){
                    $(el).tooltip({title: el.attributes.tooltip.value})
                })
            }, 300);
        },
        beforeDestroy: function (){
            clearInterval(this.interval)
            return true
        },
        methods: {
            buildUrl: function(task) {
                return '/task/' + task.slug
            },
            ts2date: function(ts){
                let date = new Date(ts * 1000)
                return date.toLocaleString('en-US', { hour12: false })
            },
            run: function(slug){
                let vm = this;
                vm.resource.save({slug: slug}, data={action: 'build_now'}).then(function(response) {
                    if (response.body && response.body.success){
                        let task = vm.tasks.find(x => x.slug == slug)
                        if (task){
                            vm.tasks[vm.tasks.indexOf(task)].build_now = true
                        }
                    }
                });
            }
        }
    })
});
