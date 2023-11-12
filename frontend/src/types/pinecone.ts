export interface ScoredVector {
  /**
   * This is the vector's unique id.
   * @type {string}
   * @memberof ScoredVector
   */
  id: string;
  /**
   * This is a measure of similarity between this vector and the query vector.  The higher the score, the more they are similar.
   * @type {number}
   * @memberof ScoredVector
   */
  score?: number;
  /**
   * This is the vector data, if it is requested.
   * @type {Array<number>}
   * @memberof ScoredVector
   */
  values?: Array<number>;
  /**
   * This is the metadata, if it is requested.
   * @type {object}
   * @memberof ScoredVector
   */
  metadata?: object;
}
