import * as d3 from 'd3';
import contextMenu from 'd3-context-menu';
import 'd3-context-menu/css/d3-context-menu.css';
import { select } from 'd3-selection';
import { scaleSequential } from 'd3-scale';
import { interpolateGreens } from 'd3-scale-chromatic';
import { transition } from 'd3-transition';
import { easeLinear } from 'd3-ease';
import { d3adaptor } from 'webcola';

import { action,
         store,
         observeStore } from './redux';

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

export class Graph {
  constructor (el, options) {
    // Set up some options.
    this.el = el;
    this.pad = 4;
    this.width = options.width || 960;
    this.height = options.height || 540;
    this.maxdepth = options.maxdepth;

    // Grab the SVG element.
    this.svg = select(el)
      .attr('width', this.width)
      .attr('height', this.height);

    // Create the cola object.
    this.cola = d3adaptor(d3)
      .size([this.width, this.height]);

    // Set starting parameters for cola.
    this.none = 10;
    this.user = 20;
    this.all = 20;

    // Empty the container.
    this.empty();

    // Subscribe to changes in the graph data.
    observeStore(next => {
      const graph = next.get('graph').toJS();
      window.setTimeout(() => {
        this.update(graph.nodes, graph.links);
      }, 0);
    }, s => s.get('graph'));

    // Subscribe to changes in the window size.
    observeStore(next => {
      const size = next.get('size').toJS();
      window.setTimeout(() => {
        this.cola.size([size.width, size.height])
          .start();

        select(this.el)
          .attr('width', size.width)
          .attr('height', size.height);
      }, 0);
    }, s => s.get('size'));
  }

  filterHidden (nodes, links) {
    const nodetable = nodes.map(x => x.key);

    const newNodes = [...nodes].filter(x => !x.hidden);
    let newLinks = links.filter(x => {
      const sourceIndex = x.source.index === undefined ? x.source : x.source.index;
      const targetIndex = x.target.index === undefined ? x.target : x.target.index;
      return !nodes[sourceIndex].hidden && !nodes[targetIndex].hidden;
    });

    let newNodetable = {};
    newNodes.forEach((x, i) => newNodetable[x.key] = i);

    newLinks.map(x => Object.assign(x, {source: newNodetable[nodetable[x.source]], target: newNodetable[nodetable[x.target]]}));

    return {
      nodes: newNodes,
      links: newLinks
    };
  }

  empty () {
    // Empty the sub-containers.
    ['.nodes', '.links', '.cards'].forEach(s => {
      this.svg.select(s)
        .selectAll('*')
        .remove();
    });
  }

  update (nodes_, links_) {
    const { nodes, links } = this.filterHidden(nodes_, links_);

    // Fade-out transition.
    const t = transition()
      .duration(500)
      .ease(easeLinear);

    // Set up the links.
    let link = this.svg.select('.links')
      .selectAll('.link')
      .data(links);
    link.exit()
      .remove();
    link = link.enter()
      .append('path')
      .classed('link', true)
      .merge(link);

    // Set up the labels.
    let card = this.svg.select('.cards')
      .selectAll('.card')
      .data(nodes, d => d.key);
    card.exit()
      .transition(t)
      .style('opacity', 0)
      .remove();
    card = card.enter()
      .append('text')
      .classed('card', true)
      .text(d => d.name)
      .call(this.cola.drag)
      .merge(card);

    // Update the virtual bounding box of the nodes by setting width and height
    // values (will be used by WebCola to perform overlap avoidance).
    const pad = this.pad
    card.each(function (d) {
      const box = this.getBBox();
      d.width = box.width + 2 * pad;
      d.height = box.height + 2 * pad;
    });

    // Set up the nodes.
    let node = this.svg.select('.nodes')
      .selectAll('.node')
      .data(nodes, d => d.key);
    node.exit()
      .transition(t)
      .style('opacity', 0)
      .remove();
    let depthmap = scaleSequential(interpolateGreens);
    node = node.enter()
      .append('rect')
      .classed('node', true)
      .attr('width', d => d.width)
      .attr('height', d => d.height)
      .attr('rx', 5)
      .attr('ry', 5)
      .style('fill', d => depthmap(d.depth / this.maxdepth))
      .call(this.cola.drag)
      .on('contextmenu', contextMenu([
        {
          title: 'Hide this node',
          action: (d, i) => {
            store.dispatch(action.toggleHide(i));
            store.dispatch(action.savePositions(node.data()));
          }
        }
      ]))
      .merge(node);

    // Launch the layout engine.
    this.cola.nodes(nodes)
      .links(links)
      .groups([])
      .linkDistance(50)
      .avoidOverlaps(true)
      .flowLayout('y', 50)
      .handleDisconnected(false)
      .start(this.none, this.user, this.all);

    // Reset the starting parameters once bootstrapped.
    this.none = this.user = this.all = 0;

    // Place elements where they should be as things are dragged around, etc.
    this.cola.on('tick', () => {
      link.attr('d', d => computePath(d.source, d.target));

      node.attr('x', d => d.x - d.width / 2)
        .attr('y', d => d.y - d.height / 2);

      card.attr('x', d => d.x - d.width / 2 + this.pad)
        .attr('y', d => d.y + d.height / 4 - this.pad);
    });
  }
}
