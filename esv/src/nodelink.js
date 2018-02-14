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
  // Set up some options.
  const pad = 4;
  const width = options.width || 960;
  const height = options.height || 540;
  const nodes = options.nodes;
  const links = options.links;

  // Grab the SVG element.
  const svg = select(el)
    .attr('width', width)
    .attr('height', height);

  // Empty the sub-containers.
  ['.nodes', '.links', '.labels'].forEach(s => {
    svg.select(s)
      .selectAll('*')
      .remove();
  });

  // Set up the links.
  let link = svg.select('.links')
    .selectAll('.link')
    .data(links);
  link = link.enter()
    .append('path')
    .classed('link', true)
    .style('fill', '#333')
    .merge(link);

  // Set up the labels.
  let label = svg.select('.labels')
    .selectAll('.label')
    .data(nodes);
  label = label.enter()
    .append('text')
    .classed('label', true)
    .style('cursor', 'move')
    .text(d => d.name)
    .merge(label);

  // Update the virtual bounding box of the nodes by setting width and height
  // values (will be used by WebCola to perform overlap avoidance).
  label.each(function (d) {
    const box = this.getBBox();
    d.width = box.width + 2 * pad;
    d.height = box.height + 2 * pad;
  });

  // Set up the nodes.
  let node = svg.select('.nodes')
    .selectAll('.node')
    .data(nodes);
  node = node.enter()
    .append('rect')
    .classed('node', true)
    .style('stroke', 'black')
    .style('stroke-width', '1.5px')
    .style('cursor', 'move')
    .attr('width', d => d.width)
    .attr('height', d => d.height)
    .attr('rx', 5)
    .attr('ry', 5)
    .style('fill', '#aaa')
    .merge(node);

  // Create the cola object.
  const cola = d3adaptor(d3)
    .linkDistance(100)
    .avoidOverlaps(true)
    .flowLayout('y', 50)
    .size([width, height]);

  // Make the nodes and labels draggable.
  node.call(cola.drag);
  label.call(cola.drag);

  // Launch the layout engine.
  cola.nodes(nodes)
    .links(links)
    .start(10, 20, 20);

  // Place elements where they should be as things are dragged around, etc.
  cola.on('tick', () => {
    link.attr('d', d => computePath(d.source, d.target));

    node.attr('x', d => d.x - d.width / 2)
      .attr('y', d => d.y - d.height / 2);

    label.attr('x', d => d.x - d.width / 2 + pad)
      .attr('y', d => d.y + d.height / 4 - pad);
  });
}
