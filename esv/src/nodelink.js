import * as d3 from 'd3';
import { select } from 'd3-selection';
import { d3adaptor } from 'webcola';

function distance (a, b) {
  const d = {
    x: b.x - a.x,
    y: b.y - a.y
  };
  return Math.sqrt(d.x * d.x + d.y * d.y);
}

function computePath (s, t) {
  const d = distance(s, t);
  const size = 5;
  const v = {
    y: -(t.x - s.x) * size / d,
    x: (t.y - s.y) * size / d
  };

  return `M${t.x} ${t.y} L${s.x + v.x} ${s.y + v.y} L${s.x - v.x} ${s.y - v.y} Z`;
}

export function makeGraph (el, options) {
  const width = options.width || 960;
  const height = options.height || 540;
  const nodes = options.nodes;
  const links = options.links;

  select(el)
    .selectAll('*')
    .remove();

  const svg = select(el)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .append('g');

  const cola = d3adaptor(d3)
    .linkDistance(100)
    .avoidOverlaps(true)
    .flowLayout('y', 150)
    .size([width, height]);

  let link = svg.selectAll('.link')
    .data(links);
  link = link.enter()
    .append('path')
    .classed('link', true)
    .style('fill', '#333')
    .merge(link);

  const rectWidth = 100;
  const rectHeight = 50;
  const pad = 5;

  let node = svg.selectAll('.node')
    .data(nodes);
  node = node.enter()
    .append('rect')
    .classed('node', true)
    .style('stroke', 'black')
    .style('stroke-width', '1.5px')
    .style('cursor', 'move')
    .attr('width', rectWidth - 2 * pad)
    .attr('height', rectHeight - 2 * pad)
    .attr('rx', 5)
    .attr('ry', 5)
    .style('fill', 'firebrick')
    .call(cola.drag)
    .merge(node);

  nodes.forEach(n => {
    n.height = rectHeight;
    n.width = rectWidth;
  });

  let label = svg.selectAll('.label')
    .data(nodes);
  label = label.enter()
    .append('text')
    .classed('label', true)
    .text(d => d.name)
    .call(cola.drag)
    .merge(label);

  cola.nodes(nodes)
    .links(links)
    .start(10, 20, 20);

  cola.on('tick', () => {
    link.attr('d', d => computePath(d.source, d.target));

    node.attr('x', d => d.x - rectWidth / 2 + pad)
      .attr('y', d => d.y - rectHeight / 2 + pad);

    label.attr('x', function (d) {
      return d.x - this.getBBox().width / 2;
    })
      .attr('y', function (d) {
        return d.y + this.getBBox().height / 4;
      });
  });
}
