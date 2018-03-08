/**
 * @desc: Tableタグのtrにリンク先が設定されていれば一行を選択可能にする
 */
export default class RowClickabler {
  constructor() {
    this.$target = $('.j-row-clickable').find('[data-href]');

    this.$target.on({
      'click': (event) => {
        this.movePage(event.currentTarget);
      }
    });
  }

  /**
   * @desc クリックされた要素のdata-hrefを取得し、そのURLに遷移する
   * @param {object} clickedTarget
   */
  movePage(clickedTarget) {
    window.location = $(clickedTarget).attr('data-href');
  };
}
