 // A FEW CONSTS
    var NUM_POINTS = 50;
    var MAX_THETA = 2*Math.PI;
    var DTHETA = MAX_THETA/NUM_POINTS;
    var WIDTH=600, HEIGHT=600;
    var i=0, data = [];
    // ... 
    for(i=0; i<NUM_POINTS; i++){
        var theta = i*DTHETA;
        data.push({theta:theta, c: Math.cos(theta), s:Math.sin(theta)});
    } 
    // SET OUR SCALES USING D3 
    var yScale = d3.scale.linear()
        .domain([0, NUM_POINTS])
        .range([0, HEIGHT]);
    // ...
    var dlines = d3.select('#chart').selectAll('data-line').data(data);
    // ADD OUR DATA TO THE DOM 
    dlines = dlines.enter().append('g')
        .classed('data-point', true);

    dlines.each(function(d, i) {
        var s, c, t;
        var g = d3.select(this);
        s = g.append('text').classed('s', true).text(d.s.toPrecision(3));
        c = g.append('text').classed('c', true).text(d.c.toPrecision(3));
        t = g.append('text').classed('t', true).text(d.theta.toPrecision(3));
    });
    // OUR MAIN UPDATE FUNCTION 
    kcharts.update = function(updateType) {
        dlines.each(function(d,i){
            var tr, tx, ty, cx, cy, sx, sy;
            var g = d3.select(this);
            switch(updateType){
            case 'ordered':
    // ... 
            case 'orig':
    // ... 
            case 'alt': // USING D3 SCALES TO CREATE SIN+COSINE WAVES
                tr = -45; tx = xThetaScale(d.theta); ty = HEIGHT+20;
                cx = xThetaScale(d.theta); cy = yThetaScale(d.c);
                sx = xThetaScale(d.theta); sy = yThetaScale(d.s);
                break;
            }
    // ... APPLY TRANSITIONS
            g.select('.t')
                .transition().duration(3000)
                .attr('transform', 'translate(' + tx + ',' + ty + ') rotate(' + tr + ')'); 
    // ...
        });
    };
    // ADD CONTROLS
    d3.select('#control-buttons').selectAll('buttons')
        .data(['ordered', 'orig', 'alt']).enter()
        .append('button').text(function(d) {
            return d;
        })
        .on('click', function(d) {
            kcharts.update(d);
        });
    // SET DEFAULT 
    kcharts.update('ordered');