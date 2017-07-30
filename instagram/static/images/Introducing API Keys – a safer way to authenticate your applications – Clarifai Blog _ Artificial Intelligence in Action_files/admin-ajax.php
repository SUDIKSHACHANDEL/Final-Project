
                if (window.addthis_product === undefined) {
                    window.addthis_product = "wpwt";
                }

                if (window.wp_product_version === undefined) {
                    window.wp_product_version = "wpwt-1.1.2";
                }

                if (window.wp_blog_version === undefined) {
                    window.wp_blog_version = "4.4.2";
                }

                if (window.addthis_share === undefined) {
                    window.addthis_share = {"passthrough":{"twitter":{"via":"Clarifai"}},"url_transforms":{"shorten":{"twitter":"bitly"}},"shorteners":{"bitly":{}}};
                }

                if (window.addthis_config === undefined) {
                    window.addthis_config = {"data_track_clickback":true,"ui_atversion":"300","data_track_addressbar":true};
                }

                if (window.addthis_layers === undefined) {
                    window.addthis_layers = {};
                }

                if (window.addthis_layers_tools === undefined) {
                    window.addthis_layers_tools = [];
                } else {
                    
                }


                if (window.addthis_plugin_info === undefined) {
                    window.addthis_plugin_info = {"info_status":"enabled","cms_name":"WordPress","cms_version":"4.4.2","plugin_name":"Website Tools by AddThis","plugin_version":"1.1.2","plugin_mode":"AddThis","anonymous_profile_id":"wp-55bc528b6f386ffb951049eaac6c282e","page_info":{"template":false}};
                }

                
                    (function() {
                      var first_load_interval_id = setInterval(function () {
                        if (typeof window.addthis !== 'undefined') {
                          window.clearInterval(first_load_interval_id);
                          window.addthis.layers(window.addthis_layers);
                          for (i = 0; i < window.addthis_layers_tools.length; i++) {
                            window.addthis.layers(window.addthis_layers_tools[i]);
                          }
                        }
                     },1000)
                    }());
                
            