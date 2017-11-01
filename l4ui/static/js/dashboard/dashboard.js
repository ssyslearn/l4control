var _dashboard = {
    init : function() {
        _dashboard.initButton();
        _dashboard.initRegion();
        _dashboard.getTotalSummary();
        _dashboard.getVMStatistics();
        _dashboard.getPlatformSummary('all');
        _dashboard.getRegionSummary();

        Highcharts.setOptions({
            global : {
                useUTC: false
            }
        });
    },

    initButton : function() {
        var vm_statistics_type = $('#dashboard-vm-statistics-type');
        vm_statistics_type.find('li a').click(function(){
            vm_statistics_type.find('li').removeClass('active');
            $('#dashboard-vm-statistics-type-text').text($(this).text());
            $(this).parent('li').addClass('active');

            _dashboard.getVMStatistics();
        });
    },

    initRegion : function() {
        var request = $.ajax({
            url: '/web/infra/ajax/list_regions',
            type: 'POST'
        });

        request.done(function(data) {
            if(data.status)
            {
                var private_region_prefix = 'KR';

                var platform_region_type = $('#dashboard-platform-region-type');

                $.each(data.response.results, function(i, item){
                    var platform_li = $('<li>').html('<a search-type="' + item.id + '">' + item.description + ' (' + item.name + ')</a>');
                    platform_region_type.append(platform_li);
                });

                platform_region_type.find('li a').click(function(){
                    platform_region_type.find('li').removeClass('active');
                    $('#dashboard-platform-region-type-text').text($(this).text());
                    $(this).parent('li').addClass('active');

                    _dashboard.getPlatformSummary($(this).attr('search-type'));
                });
            }
        });
    },

    getTotalSummary : function() {
        var request = $.ajax({
            url: '/web/dashboard/ajax/get_total_summary',
            type: 'POST',
            beforeSend: function(xhr, settings) {
                $('#dashboard-alert-panel').hide();
            }
        });

        request.done(function(data) {
            if(data.status)
            {
                var vm_count = new CountUp('dashboard-vm-count', 0, data.response.vm_count, 0, 1);
                var unregistered_vm_count = new CountUp('dashboard-unregistered-vm-count', 0, data.response.unregistered_vm_count, 0, 1);
                var notcreated_vm_count = new CountUp('dashboard-notcreated-vm-count', 0, data.response.notcreated_vm_count, 0, 1);
                var host_count = new CountUp('dashboard-host-count', 0, data.response.host_count, 0, 1);
                var storage_count = new CountUp('dashboard-storage-count', 0, data.response.storage_count, 0, 1);
                var service_count = new CountUp('dashboard-service-count', 0, data.response.service_count, 0, 1);

                vm_count.start();
                unregistered_vm_count.start();
                notcreated_vm_count.start();
                host_count.start();
                storage_count.start();
                service_count.start();

                if(data.response.unregistered_vm_count > 0)
                {
                    $('#dashboard-unregistered-vm-count-alert').show();
                }

                if(data.response.notcreated_vm_count > 0)
                {
                    $('#dashboard-notcreated-vm-count-alert').show();
                }
            }
            else
            {
                $('#dashboard-alert-panel').html('<strong>Failed to load :</strong> ' + data.message);
                $('#dashboard-alert-panel').show();
            }
        });

		request.fail(function(jqXHR, textStatus, errorThrown) {
            $('#dashboard-alert-panel').html('<strong>Failed to load :</strong>' + jqXHR.status + ' ' + jqXHR.responseText);
            $('#dashboard-alert-panel').show();
		});
    },

    getVMStatistics : function() {
        var request = $.ajax({
            url: '/web/dashboard/ajax/get_vm_statistics',
            type: 'POST',
            data: {
                vm_type: $('#dashboard-vm-statistics-type .active a').attr('search-type')
            }
        });

        request.done(function(data) {
            if(data.status)
            {
                var chart_data = data.response.results;

                $('#dashboard-vm-statistics-chart').highcharts({
                    chart: {
                        type: 'line'
                    },
                    title: {
                        text: ''
                    },
                    xAxis: {
                        type: 'datetime',
                        gridLineWidth: 1,
                        dateTimeLabelFormats: {
                            millisecond: '%m/%d',
                            second: '%m/%d',
                            minute: '%m/%d',
                            hour: '%m/%d',
                            day: '%m/%d',
                            month: '%m/%d',
                            year: '%m'
                        }
                    },
                    yAxis: {
                        allowDecimals: false,
                        title: {
                            text: ''
                        }
                    },
                    tooltip: {
                        headerFormat: '<span style="font-size: 10px">{point.key:%m/%d}</span><br/>'
                    },
                    credits: {
                        enabled: false
                    },
                    legend: {
                        enabled: false
                    },
                    plotOptions: {
                        area: {
                            marker: {
                                lineWidth: 1,
                                lineColor: '#ffffff'
                            },
                            fillOpacity: 0.4,
                            threshold: null
                        }
                    },
                    series: [{
                        name:'VM Count',
                        type: 'area',
                        data: chart_data
                    }]
                });
            }
        });
    },

    getPlatformSummary : function(region_id) {
        var request = $.ajax({
            url: '/web/dashboard/ajax/get_platform_summary',
            type: 'POST',
            data: {
                region_id: region_id
            }
        });

        request.done(function(data) {
            if(data.status)
            {
                var graph_data = new Array();

                $.each(data.response.platforms, function(i, item){
                    if(item.vm_count > 0)
                    {
                        var item_name = 'Unknown';
                        var item_color = '5e5e5e';
                        if(i == 'vsphere')
                        {
                            item_name = 'vSphere';
                            item_color = '#337ab7';
                        }
                        else if(i == 'vcloud')
                        {
                            item_name = 'vCloud';
                            item_color = '#5bc0de';
                        }
                        else if(i == 'openstack')
                        {
                            item_name = 'OpenStack';
                            item_color = '#d9534f';
                        }
                        else if (i == 'aws')
                        {
                            item_name = 'AWS';
                            item_color = '#f0ad4e';
                        }

                        graph_data.push({
                            name: item_name,
                            color: item_color,
                            y: item.vm_count,
                            link: '/web/infra/vm?platform_type=' + i + ((region_id != 'all')?'&region_id=' + region_id:'')
                        });
                    }
                });

                $('#dashboard-platform-data').empty();
                $('#dashboard-platform-chart').highcharts({
                    chart: {
                        plotBackgroundColor: null,
                        plotBorderWidth: null,
                        plotShadow: false,
                        type: 'pie'
                    },
                    title: {
                        text: ''
                    },
                    tooltip: {
                        pointFormat: '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.y}</b> ({point.percentage:.1f}%)<br/>'
                    },
                    credits: {
                        enabled: false
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            innerSize: '60%',
                            dataLabels: {
                                enabled: false
                            }
                        }
                    },
                    series: [{
                        name: "Count",
                        colorByPoint: true,
                        data: graph_data
                    }]
                }, function(chart){
                    $(chart.series).each(function(i, serie) {
                        var vm_region_data = $('#dashboard-platform-data');
                        $.each(serie.data, function(i, item) {
                            var item_data = $('<div class="legend" style="border-left:7px solid ' + item.color + ';">').append(
                                $('<div class="legend-title">').html(item.name),
                                $('<div class="legend-data">').html('<a href="' + item.link + '" target="_blank">' + item.y + '</a>')
                            );
                            vm_region_data.append(item_data);
                        });
                    });
                });
            }
        });
    },

    getRegionSummary : function() {
        var request = $.ajax({
            url: '/web/dashboard/ajax/get_region_summary',
            type: 'POST'
        });

        request.done(function(data) {
            if(data.status)
            {

                var regions = data.response.regions;
                var graph_data = new Array();

                $.each(regions, function(i, item){
                    if(item.vm_count > 0)
                    {
                        graph_data.push({
                            name: item.description + ' (' + i + ')',
                            y: item.vm_count,
                            link: '/web/infra/vm?region_id=' + item.id
                        });
                    }
                });

                $('#dashboard-region-data').empty();
                $('#dashboard-region-chart').highcharts({
                    chart: {
                        plotBackgroundColor: null,
                        plotBorderWidth: null,
                        plotShadow: false,
                        type: 'pie'
                    },
                    colors: ["#DDDF0D", "#7798BF", "#55BF3B", "#DF5353", "#AAEEEE", "#FF0066", "#EEAAEE", "#55BF3B", "#DF5353", "#7798BF", "#AAEEEE"],
                    title: {
                        text: ''
                    },
                    tooltip: {
                        pointFormat: '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.y}</b> ({point.percentage:.1f}%)<br/>'
                    },
                    credits: {
                        enabled: false
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            innerSize: '60%',
                            dataLabels: {
                                enabled: false
                            }
                        }
                    },
                    series: [{
                        name: "Count",
                        colorByPoint: true,
                        data: graph_data
                    }]
                }, function(chart){
                    $(chart.series).each(function(i, serie) {
                        var vm_region_data = $('#dashboard-region-data');
                        $.each(serie.data, function(i, item) {
                            var item_data = $('<div class="legend" style="border-left:7px solid ' + item.color + ';">').append(
                                $('<div class="legend-title" title="' + item.name + '">').html(item.name),
                                $('<div class="legend-data">').html('<a href="' + item.link + '" target="_blank">' + item.y + '</a>')
                            );
                            vm_region_data.append(item_data);
                        });
                    });
                });
            }
        });
    }
};